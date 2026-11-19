#!/bin/bash
# ==============================================================================
# GCP Spot VM Self-Terminating PLE Runner
# - Clones benchmark evaluator (google-research/ple)
# - Clones debim-ple-harness (feature/antigravity-sdk)
# - Automatically downloads task files from Hugging Face
# - Runs evaluation under Stage 2 constraints (2 CPUs, 4 GB RAM, 6-Hour limit)
# - Syncs results & artifacts to Google Cloud Storage (GCS)
# - Self-deletes VM immediately after run to minimize cost (~1-4 THB per task)
# ==============================================================================

set -x

export DEBIAN_FRONTEND=noninteractive

# 1. Retrieve VM metadata
METADATA_URL="http://metadata.google.internal/computeMetadata/v1"
ZONE=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/zone" | awk -F/ '{print $NF}')
NAME=$(hostname)
PROJECT_ID=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/project/project-id")

# Fetch custom bucket from metadata if provided, otherwise default
GCS_BUCKET=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/gcs-bucket" 2>/dev/null)
if [ -z "$GCS_BUCKET" ] || [[ "$GCS_BUCKET" == *"404"* ]]; then
  GCS_BUCKET="gs://${PROJECT_ID}-ple-results"
fi

TASK_NAME=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/task-name" 2>/dev/null)
if [ -z "$TASK_NAME" ] || [[ "$TASK_NAME" == *"404"* ]]; then
  TASK_NAME="footing-settlement-verification"
fi

API_KEY=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/gemini-api-key" 2>/dev/null)
HF_TOKEN=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/hf-token" 2>/dev/null)

if [ -z "$API_KEY" ] || [[ "$API_KEY" == *"404"* ]]; then
  echo "ERROR: gemini-api-key not found in metadata" >&2
  exit 1
fi

WORKDIR="/opt/benchmark"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# 2. Install Dependencies (Docker, git, curl, uv)
apt-get update -y
apt-get install -y docker.io git curl
systemctl start docker

curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/root/.local/bin:$PATH"

# 3. Clone Repositories
git clone https://github.com/google-research/ple.git ple || true
git clone -b feature/antigravity-sdk https://github.com/PRIDA-TAKON/debim-ple-harness.git debim-ple-harness || true

# 4. Prepare Environment & API Key
cd "$WORKDIR/ple"
cat <<EOF > .env
HF_TOKEN=${HF_TOKEN}
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
VERTEXAI_PROJECT=${PROJECT_ID}
EOF

# Ensure debim-ple-harness also has .env
cat <<EOF > "$WORKDIR/debim-ple-harness/.env"
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
EOF

# 5. Run Evaluation via PLE Benchmark (Automatically downloads task files from Hugging Face)
echo "=== Starting PLE Evaluation for task: ${TASK_NAME} ==="
# Timeout 350m (5h 50m) to preserve last 10m for GCS sync and self-deletion
timeout 350m uv run python eval/run.py ../debim-ple-harness --tasks "${TASK_NAME}" --env-file .env || echo "Execution finished or timeout reached."

# 6. Upload Results & Artifacts to Google Cloud Storage
echo "=== Uploading results to ${GCS_BUCKET}/${TASK_NAME} ==="
if [ -d "runs" ]; then
  gsutil -m cp -r runs/ "${GCS_BUCKET}/${TASK_NAME}/runs" || true
fi
if [ -d "../debim-ple-harness/artifacts" ]; then
  gsutil -m cp -r ../debim-ple-harness/artifacts/ "${GCS_BUCKET}/${TASK_NAME}/artifacts" || true
fi

# 7. Self-destruct VM immediately to prevent any extra charges
echo "=== Finished! Self-deleting VM ${NAME} in zone ${ZONE} ==="
gcloud --quiet compute instances delete "$NAME" --zone="$ZONE"

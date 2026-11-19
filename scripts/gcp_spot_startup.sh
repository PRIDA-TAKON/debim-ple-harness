#!/bin/bash
# ==============================================================================
# GCP Spot VM Self-Terminating PLE Runner
# - Clones benchmark evaluator (google-research/ple)
# - Clones debim-ple-harness (feature/antigravity-sdk)
# - Starts LiteLLM Proxy for Google-Cloud models
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

# 2. Install Dependencies (Docker, git, curl, uv, python3, iptables)
apt-get update -y
apt-get install -y git curl python3 iptables

# Set iptables to legacy mode on Debian 12 to ensure Docker bridge networking creates NAT/Gateway
update-alternatives --set iptables /usr/sbin/iptables-legacy || true
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy || true

# Explicitly configure Docker default bridge with 172.17.0.1 gateway
mkdir -p /etc/docker
cat <<EOF > /etc/docker/daemon.json
{
  "bip": "172.17.0.1/16"
}
EOF

# Install Docker CE
curl -fsSL https://get.docker.com | sh || apt-get install -y docker.io
systemctl restart docker

# Verify Docker bridge gateway is active
echo "Docker bridge gateway:"
docker network inspect bridge --format "{{range .IPAM.Config}}{{.Gateway}} {{end}}"

# Install uv and link to system path
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/root/.local/bin:$PATH"
ln -sf /root/.local/bin/uv /usr/local/bin/uv

# Install Harbor 0.20.0 with websockets (strictly required by PLE eval/run.py)
uv tool install harbor==0.20.0 --with websockets
ln -sf /root/.local/bin/harbor /usr/local/bin/harbor

# 3. Clone Repositories
git clone https://github.com/google-research/ple.git ple || true
git clone -b feature/antigravity-sdk https://github.com/PRIDA-TAKON/debim-ple-harness.git debim-ple-harness || true

# 4. Prepare Environment & Start LiteLLM Model Proxy
cd "$WORKDIR/ple"

PROXY_KEY="sk-debim-ple-local-proxy-key"
export MODEL_PROXY_KEY="${PROXY_KEY}"
export MODEL_PROXY_URL="http://127.0.0.1:4000"
export GEMINI_API_KEY="${API_KEY}"
export GOOGLE_API_KEY="${API_KEY}"

cat <<EOF > .env
HF_TOKEN=${HF_TOKEN}
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
MODEL_PROXY_URL=http://127.0.0.1:4000
MODEL_PROXY_KEY=${PROXY_KEY}
EOF

# Ensure debim-ple-harness also has .env
cat <<EOF > "$WORKDIR/debim-ple-harness/.env"
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
EOF

# Explicitly configure LiteLLM to use Gemini API Key (AI Studio), NOT Vertex AI
cat <<EOF > kit/model_proxy/config.yaml
model_list:
  - model_name: gemma-4-26b
    litellm_params:
      model: gemini/gemma-4-26b-a4b-it
      api_key: os.environ/GEMINI_API_KEY
  - model_name: gemini-3.8-flash
    litellm_params:
      model: gemini/gemma-4-26b-a4b-it
      api_key: os.environ/GEMINI_API_KEY
  - model_name: claude-opus-5-5
    litellm_params:
      model: gemini/gemma-4-26b-a4b-it
      api_key: os.environ/GEMINI_API_KEY
      drop_params: true
  - model_name: gemini-4-argon
    litellm_params:
      model: gemini/gemma-4-26b-a4b-it
      api_key: os.environ/GEMINI_API_KEY
  - model_name: antigravity-preview-latest
    litellm_params:
      model: gemini/gemma-4-26b-a4b-it
      api_key: os.environ/GEMINI_API_KEY

litellm_settings:
  drop_params: true
  num_retries: 3
  request_timeout: 1800
EOF

echo "=== Starting LiteLLM Model Proxy on port 4000 ==="
nohup uv run --no-project --python 3.11 --with "litellm[proxy,google]==1.90.0" litellm --config kit/model_proxy/config.yaml --host 0.0.0.0 --port 4000 > /tmp/litellm.log 2>&1 &

# Wait up to 60 seconds for LiteLLM proxy to become healthy
for i in {1..30}; do
  if curl -s http://127.0.0.1:4000/health > /dev/null 2>&1; then
    echo "LiteLLM proxy is ready and healthy!"
    break
  fi
  echo "Waiting for LiteLLM proxy... ($i/30)"
  sleep 2
done

# 5. Run Evaluation via PLE Benchmark (Automatically downloads task files from Hugging Face)
echo "=== Starting PLE Evaluation for task: ${TASK_NAME} ==="
# Timeout 350m (5h 50m) to preserve last 10m for GCS sync and self-deletion
timeout 350m uv run python eval/run.py ../debim-ple-harness --tasks "${TASK_NAME}" --env-file .env 2>&1 | tee /tmp/eval_run.log || echo "Execution finished or timeout reached."

# 6. Upload Results, Artifacts, and Logs to Google Cloud Storage
echo "=== Uploading results to ${GCS_BUCKET}/${TASK_NAME} ==="
if [ -d "runs" ]; then
  gsutil -m cp -r runs/ "${GCS_BUCKET}/${TASK_NAME}/runs" || true
fi
if [ -d "../debim-ple-harness/artifacts" ]; then
  gsutil -m cp -r ../debim-ple-harness/artifacts/ "${GCS_BUCKET}/${TASK_NAME}/artifacts" || true
fi
gsutil cp /tmp/litellm.log "${GCS_BUCKET}/${TASK_NAME}/litellm.log" || true
gsutil cp /tmp/eval_run.log "${GCS_BUCKET}/${TASK_NAME}/eval_run.log" || true

# 7. Self-destruct VM immediately to prevent any extra charges
echo "=== Finished! Self-deleting VM ${NAME} in zone ${ZONE} ==="
gcloud --quiet compute instances delete "$NAME" --zone="$ZONE"

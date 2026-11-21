#!/bin/bash
# ==============================================================================
# GCP Sharded PLE Batch Runner for Spot / On-Demand Instances
# - Model: gemma-4-26b-a4b-it-maas via Google Cloud Vertex AI (Global MaaS)
# - Reads shard tasks list and shard ID dynamically from instance metadata
# - Pre-syncs tasks cache from GCS to eliminate Hugging Face 429 rate limits
# - Real-time progress sync to gs://${PROJECT_ID}-ple-results/gemma4/
# - Auto-powers off VM upon shard completion
# ==============================================================================

set -x

export DEBIAN_FRONTEND=noninteractive

# 1. Start Safety Watchdog: 20 hours (1200 minutes) per shard
echo "=== Setting 20-hour OS Watchdog ==="
shutdown -h +1200 "PLE Shard batch runner maximum runtime reached" &

# 2. Retrieve VM metadata
METADATA_URL="http://metadata.google.internal/computeMetadata/v1"
ZONE=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/zone" | awk -F/ '{print $NF}')
NAME=$(hostname)
PROJECT_ID=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/project/project-id")

GCS_BUCKET=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/gcs-bucket" 2>/dev/null)
if [ -z "$GCS_BUCKET" ] || [[ "$GCS_BUCKET" == *"404"* ]]; then
  GCS_BUCKET="gs://${PROJECT_ID}-ple-results/gemma4"
else
  if [[ "$GCS_BUCKET" != *"/gemma4"* ]]; then
    GCS_BUCKET="${GCS_BUCKET}/gemma4"
  fi
fi

SHARD_ID=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/shard-id" 2>/dev/null)
if [ -z "$SHARD_ID" ] || [[ "$SHARD_ID" == *"404"* ]]; then
  SHARD_ID="shard-default"
fi

SHARD_TASKS_STR=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/shard-tasks" 2>/dev/null)

API_KEY=$(curl -s -f -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/gemini-api-key" 2>/dev/null || echo "")
HF_TOKEN=$(curl -s -f -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/hf-token" 2>/dev/null || echo "")

if [ -z "$API_KEY" ] || [[ "$API_KEY" == *"404"* ]] || [[ "$API_KEY" == *"<"* ]]; then
  echo "WARNING: gemini-api-key not found in metadata, using dummy fallback for Vertex AI"
  API_KEY="dummy-vertex-key"
fi

if [ -z "$HF_TOKEN" ] || [[ "$HF_TOKEN" == *"404"* ]] || [[ "$HF_TOKEN" == *"<"* ]]; then
  HF_TOKEN=""
fi

WORKDIR="/opt/benchmark"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# 3. Install Host Dependencies
apt-get update -y
apt-get install -y git curl python3 python3-pip iptables

# Legacy iptables for Docker bridge networking
update-alternatives --set iptables /usr/sbin/iptables-legacy || true
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy || true

mkdir -p /etc/docker
cat <<EOF > /etc/docker/daemon.json
{
  "bip": "172.17.0.1/16"
}
EOF

curl -fsSL https://get.docker.com | sh || apt-get install -y docker.io
systemctl restart docker

# Install uv & Harbor 0.20.0
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/root/.local/bin:$PATH"
ln -sf /root/.local/bin/uv /usr/local/bin/uv

uv tool install harbor==0.20.0 --with websockets
ln -sf /root/.local/bin/harbor /usr/local/bin/harbor

# Install google-genai for Vertex AI Client with break-system-packages
pip3 install --break-system-packages google-genai || uv pip install --system google-genai

# 4. Clone Repositories
git clone https://github.com/google-research/ple.git ple || true
git clone -b feature/antigravity-sdk https://github.com/PRIDA-TAKON/debim-ple-harness.git debim-ple-harness || true

cd "$WORKDIR/ple"

PROXY_KEY="sk-debim-ple-local-proxy-key"
export MODEL_PROXY_KEY="${PROXY_KEY}"
export MODEL_PROXY_URL="http://127.0.0.1:4000"
export GEMINI_API_KEY="${API_KEY}"
export GOOGLE_API_KEY="${API_KEY}"
export VERTEXAI_PROJECT="${PROJECT_ID}"
export VERTEXAI_LOCATION="global"
export GEMMA_MODEL="gemma-4-26b-a4b-it-maas"

cat <<EOF > .env
HF_TOKEN=${HF_TOKEN}
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
MODEL_PROXY_URL=http://127.0.0.1:4000
MODEL_PROXY_KEY=${PROXY_KEY}
VERTEXAI_PROJECT=${PROJECT_ID}
VERTEXAI_LOCATION=global
GEMMA_MODEL=gemma-4-26b-a4b-it-maas
EOF

cat <<EOF > "$WORKDIR/debim-ple-harness/.env"
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
MODEL_PROXY_URL=http://127.0.0.1:4000
MODEL_PROXY_KEY=${PROXY_KEY}
VERTEXAI_PROJECT=${PROJECT_ID}
VERTEXAI_LOCATION=global
GEMMA_MODEL=gemma-4-26b-a4b-it-maas
EOF

# 5. Restore Tasks Cache from GCS to bypass Hugging Face 429
echo "=== Restoring PLE tasks cache from GCS ==="
mkdir -p /root/.cache/plebench/
gsutil -m rsync -r "gs://${PROJECT_ID}-ple-results/cache/plebench/" /root/.cache/plebench/ 2>/dev/null || true

# 6. Start Lightweight Vertex AI Gemma 4 Proxy on port 4000
echo "=== Starting Vertex AI Gemma 4 Proxy on port 4000 ==="
nohup python3 "$WORKDIR/debim-ple-harness/scripts/vertex_gemma_proxy.py" 4000 > /tmp/proxy.log 2>&1 &

for i in {1..30}; do
  if curl -s http://127.0.0.1:4000/health > /dev/null 2>&1; then
    echo "Vertex AI Gemma 4 proxy is ready and healthy!"
    break
  fi
  echo "Waiting for Vertex AI proxy... ($i/30)"
  sleep 2
done

# 7. Canary Check Function: Verifies Vertex AI Proxy Health
check_canary_quota() {
  local http_code
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:4000/health")
  if [ "$http_code" -eq 200 ]; then
    echo "Canary Probe: HTTP 200 OK (Vertex AI Proxy Healthy)"
    return 0
  else
    echo "CRITICAL: Vertex AI Proxy unhealthy (HTTP $http_code)"
    return 1
  fi
}

# 8. Parse Tasks for this Shard
if [ -n "$SHARD_TASKS_STR" ] && [[ "$SHARD_TASKS_STR" != *"404"* ]]; then
  read -ra TASKS <<< "$SHARD_TASKS_STR"
else
  echo "No shard-tasks attribute provided, falling back to full list"
  TASKS=(
    "fill-compaction-acceptance"
    "footing-settlement-verification"
    "division-26-specifications"
    "solar-supplemental-review"
    "permission-to-operate-memo"
    "pre-application-capacity-response"
  )
fi

TOTAL_TASKS=${#TASKS[@]}
COMPLETED_COUNT=0
FAILED_COUNT=0

echo "=========================================================="
echo "Starting Execution of [$SHARD_ID] with $TOTAL_TASKS Tasks"
echo "Tasks: ${TASKS[*]}"
echo "=========================================================="

mkdir -p /tmp/eval_logs

for idx in "${!TASKS[@]}"; do
  TASK="${TASKS[$idx]}"
  TASK_NUM=$((idx + 1))
  
  echo ""
  echo "=========================================================="
  echo "[$SHARD_ID] [$TASK_NUM / $TOTAL_TASKS] Executing Task: $TASK"
  echo "Time: $(date -u)"
  echo "=========================================================="
  
  # Check if task already has a passing score (> 0) in GCS or local runs
  ALREADY_SCORED=$(python3 -c "
import json, glob, sys
task = sys.argv[1]
scored = False
for pattern in ['/opt/benchmark/ple/runs/**/' + task + '*/result*.json', '/opt/benchmark/ple/runs/**/' + task + '*/results.json']:
    for f in glob.glob(pattern, recursive=True):
        try:
            d = json.load(open(f))
            score = d.get('score') if d.get('score') is not None else d.get('metrics', {}).get('score', 0.0)
            if float(score) > 0.0:
                scored = True
                break
        except:
            pass
    if scored:
        break
print('YES' if scored else 'NO')
" "$TASK" 2>/dev/null || echo "NO")

  if [ "$ALREADY_SCORED" = "YES" ]; then
    echo "⏩ Task $TASK already has a score > 0! Skipping."
    COMPLETED_COUNT=$((COMPLETED_COUNT + 1))
    continue
  fi

  # Canary health check before running task
  if ! check_canary_quota; then
    echo "Vertex AI Proxy unhealthy! Restarting proxy..."
    nohup python3 "$WORKDIR/debim-ple-harness/scripts/vertex_gemma_proxy.py" 4000 > /tmp/proxy.log 2>&1 &
    sleep 3
  fi
  
  TASK_LOG="/tmp/eval_logs/eval_${TASK}.log"
  
  # Run Task with strict 90-minute hard timeout (90m) to prevent runaway loops
  timeout 90m uv run python eval/run.py ../debim-ple-harness --tasks "$TASK" --env-file .env 2>&1 | tee "$TASK_LOG"
  TASK_EXIT_CODE=${PIPESTATUS[0]}
  
  if [ "$TASK_EXIT_CODE" -eq 124 ]; then
    echo "⚠️ Task $TASK TIMED OUT (Reached 90-Minute Hard Limit)! Skipping to next task automatically."
    FAILED_COUNT=$((FAILED_COUNT + 1))
  elif [ "$TASK_EXIT_CODE" -ne 0 ]; then
    echo "⚠️ Task $TASK finished with error code $TASK_EXIT_CODE"
    FAILED_COUNT=$((FAILED_COUNT + 1))
  else
    echo "✅ Task $TASK finished successfully!"
    COMPLETED_COUNT=$((COMPLETED_COUNT + 1))
  fi
  
  # Sync completed run results to GCS immediately
  echo "=== Syncing $TASK results to GCS ==="
  if [ -d "runs" ]; then
    gsutil -m rsync -r runs/ "${GCS_BUCKET}/runs/" || true
  fi
  gsutil cp "$TASK_LOG" "${GCS_BUCKET}/logs/eval_${TASK}.log" || true
  gsutil cp /tmp/proxy.log "${GCS_BUCKET}/logs/proxy_${SHARD_ID}_${TASK}.log" || true
  
  # Also sync back any new cached task files to GCS cache so other workers benefit
  gsutil -m rsync -r /root/.cache/plebench/ "gs://${PROJECT_ID}-ple-results/cache/plebench/" 2>/dev/null || true
  
  # Write real-time progress file for this shard
  cat <<STATUS_EOF > "/tmp/progress_${SHARD_ID}.json"
{
  "shard_id": "$SHARD_ID",
  "current_task": "$TASK",
  "task_number": $TASK_NUM,
  "total_tasks": $TOTAL_TASKS,
  "completed_count": $COMPLETED_COUNT,
  "failed_count": $FAILED_COUNT,
  "last_updated": "$(date -u)"
}
STATUS_EOF
  gsutil cp "/tmp/progress_${SHARD_ID}.json" "${GCS_BUCKET}/progress_${SHARD_ID}.json" || true
  
  # Cleanup docker containers & build cache aggressively to prevent disk exhaustion
  echo "=== Cleaning container memory and build cache ==="
  docker rm -f $(docker ps -aq) 2>/dev/null || true
  docker builder prune -f 2>/dev/null || true
  docker system prune -f 2>/dev/null || true
done

echo "=========================================================="
echo "Shard [$SHARD_ID] finished! Completed: $COMPLETED_COUNT, Failed/Timed-out: $FAILED_COUNT"
echo "Powering off VM to terminate compute billing."
echo "=========================================================="

# Final sync and poweroff
if [ -d "runs" ]; then
  gsutil -m rsync -r runs/ "${GCS_BUCKET}/runs/" || true
fi
poweroff

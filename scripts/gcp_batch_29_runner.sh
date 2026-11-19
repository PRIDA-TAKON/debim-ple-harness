#!/bin/bash
# ==============================================================================
# GCP On-Demand (Standard) 29-Task Sequential PLE Batch Runner
# - Model: gemma-4-26b-a4b-it on Google AI Studio Paid Tier
# - Sequential execution of all 29 PLE-Bench tasks
# - Per-Task Hard Timeout: Max 6 hours (360m)
# - Canary Probe: Pre-checks AI Studio credit before each task; shuts down VM if exhausted
# - OS-Level Watchdog: 29 hours (1740 minutes) automatic shutdown
# - Real-time GCS Sync after each task completion
# - Self-termination (poweroff) upon completion
# ==============================================================================

set -x

export DEBIAN_FRONTEND=noninteractive

# 1. Start OS-Level Watchdog: 29 hours (1740 minutes)
echo "=== Setting 29-hour OS Watchdog ==="
shutdown -h +1740 "PLE 29-Task batch runner maximum runtime reached" &

# 2. Retrieve VM metadata
METADATA_URL="http://metadata.google.internal/computeMetadata/v1"
ZONE=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/zone" | awk -F/ '{print $NF}')
NAME=$(hostname)
PROJECT_ID=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/project/project-id")

GCS_BUCKET=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/gcs-bucket" 2>/dev/null)
if [ -z "$GCS_BUCKET" ] || [[ "$GCS_BUCKET" == *"404"* ]]; then
  GCS_BUCKET="gs://${PROJECT_ID}-ple-results"
fi

API_KEY=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/gemini-api-key" 2>/dev/null)
HF_TOKEN=$(curl -s -H "Metadata-Flavor: Google" "$METADATA_URL/instance/attributes/hf-token" 2>/dev/null)

if [ -z "$API_KEY" ] || [[ "$API_KEY" == *"404"* ]]; then
  echo "ERROR: gemini-api-key not found in metadata" >&2
  poweroff
  exit 1
fi

WORKDIR="/opt/benchmark"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# 3. Install Host Dependencies
apt-get update -y
apt-get install -y git curl python3 iptables

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

# 4. Clone Repositories
git clone https://github.com/google-research/ple.git ple || true
git clone -b feature/antigravity-sdk https://github.com/PRIDA-TAKON/debim-ple-harness.git debim-ple-harness || true

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

cat <<EOF > "$WORKDIR/debim-ple-harness/.env"
GEMINI_API_KEY=${API_KEY}
GOOGLE_API_KEY=${API_KEY}
EOF

# 5. Configure LiteLLM Model Proxy for gemma-4-26b-a4b-it (Google AI Studio)
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

for i in {1..30}; do
  if curl -s http://127.0.0.1:4000/health > /dev/null 2>&1; then
    echo "LiteLLM proxy is ready and healthy!"
    break
  fi
  echo "Waiting for LiteLLM proxy... ($i/30)"
  sleep 2
done

# 6. Canary Check Function: Verifies AI Studio Credit / Quota
check_canary_quota() {
  local http_code
  http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://generativelanguage.googleapis.com/v1beta/models/gemma-4-26b-a4b-it:generateContent?key=${API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"contents":[{"parts":[{"text":"ping"}]}]}')
  
  if [ "$http_code" -eq 200 ]; then
    echo "Canary Probe: HTTP 200 OK (Quota Healthy)"
    return 0
  elif [ "$http_code" -eq 429 ] || [ "$http_code" -eq 402 ]; then
    echo "CRITICAL: Canary Probe returned HTTP $http_code (AI Studio Quota/Credit EXHAUSTED)!"
    return 1
  else
    echo "Canary Probe: HTTP $http_code (Proceeding with caution)"
    return 0
  fi
}

# 7. Ordered List of All 29 Tasks
TASKS=(
  "fill-compaction-acceptance"
  "footing-settlement-verification"
  "division-26-specifications"
  "solar-supplemental-review"
  "permission-to-operate-memo"
  "pre-application-capacity-response"
  "backfeed-energization-reply"
  "solar-witness-test-package"
  "lv-cable-sizing"
  "engineers-estimate-check"
  "emergency-spillway-check"
  "landscape-sheet-revision"
  "heat-rejection-life-cycle-cost"
  "cooling-water-flush-plan"
  "wind-diaphragm-shear"
  "seismic-diaphragm-shear"
  "roof-deck-design"
  "data-hall-mep-routing"
  "data-hall-mep-routing-offset"
  "data-center-site-model"
  "fire-test-validation-memo"
  "fire-solve-convergence"
  "les-mesh-resolution"
  "eor-review-corrections"
  "foundation-strategy"
  "frame-extension-method"
  "mv-conveyance-study"
  "data-hall-device-takeoff"
  "shoring-design-verification"
)

TOTAL_TASKS=${#TASKS[@]}
COMPLETED_COUNT=0
FAILED_COUNT=0

echo "=========================================================="
echo "Starting Execution of $TOTAL_TASKS Tasks Sequentially"
echo "=========================================================="

mkdir -p /tmp/eval_logs

for idx in "${!TASKS[@]}"; do
  TASK="${TASKS[$idx]}"
  TASK_NUM=$((idx + 1))
  
  echo ""
  echo "=========================================================="
  echo "[$TASK_NUM / $TOTAL_TASKS] Executing Task: $TASK"
  echo "Time: $(date -u)"
  echo "=========================================================="
  
  # Check if task already has a passing score (> 0) in previous runs - skip if already scored
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
    echo "⏩ Task $TASK already has a score > 0! Skipping as requested by user."
    COMPLETED_COUNT=$((COMPLETED_COUNT + 1))
    continue
  fi

  # Canary credit check before running task
  if ! check_canary_quota; then
    echo "AI Studio Credit Exhausted! Halting batch execution."
    echo "Credit exhausted at task $TASK ($TASK_NUM / $TOTAL_TASKS)" > /tmp/CREDIT_EXHAUSTED.txt
    gsutil cp /tmp/CREDIT_EXHAUSTED.txt "${GCS_BUCKET}/CREDIT_EXHAUSTED.txt" || true
    break
  fi
  
  TASK_LOG="/tmp/eval_logs/eval_${TASK}.log"
  
  # Run Task with strict 6-hour timeout (360m)
  timeout 360m uv run python eval/run.py ../debim-ple-harness --tasks "$TASK" --env-file .env 2>&1 | tee "$TASK_LOG"
  TASK_EXIT_CODE=${PIPESTATUS[0]}
  
  if [ "$TASK_EXIT_CODE" -eq 124 ]; then
    echo "⚠️ Task $TASK TIMED OUT (Reached 6-Hour Hard Limit)!"
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
  gsutil cp /tmp/litellm.log "${GCS_BUCKET}/logs/litellm_${TASK}.log" || true
  
  # Write real-time progress file
  cat <<STATUS_EOF > /tmp/progress.json
{
  "current_task": "$TASK",
  "task_number": $TASK_NUM,
  "total_tasks": $TOTAL_TASKS,
  "completed_count": $COMPLETED_COUNT,
  "failed_count": $FAILED_COUNT,
  "last_updated": "$(date -u)"
}
STATUS_EOF
  gsutil cp /tmp/progress.json "${GCS_BUCKET}/progress.json" || true
  
  # Cleanup docker containers & unused build cache to preserve disk space
  echo "=== Cleaning container memory and dangling volumes ==="
  docker rm -f $(docker ps -aq) 2>/dev/null || true
  docker builder prune -f --filter "until=2h" 2>/dev/null || true
done

echo "=========================================================="
echo "All tasks finished or stopped. Total completed: $COMPLETED_COUNT, Failed/Timed-out: $FAILED_COUNT"
echo "Powering off VM to terminate compute billing."
echo "=========================================================="

# Final sync and poweroff
if [ -d "runs" ]; then
  gsutil -m rsync -r runs/ "${GCS_BUCKET}/runs/" || true
fi
poweroff

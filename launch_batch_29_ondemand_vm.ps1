param (
    [string]$Zone = "us-central1-c",
    [string]$MachineType = "e2-standard-4",
    [string]$Bucket = "gs://lab-ai-972593-ple-results"
)

$InstanceName = "ple-batch29-$(Get-Date -Format 'MMdd-HHmm')"
$StartupScript = Join-Path $PSScriptRoot "scripts\gcp_batch_29_runner.sh"

# Read API Key from local .env
$ApiKey = ""
$EnvPath = Join-Path $PSScriptRoot ".env"
if (Test-Path $EnvPath) {
    Get-Content $EnvPath | ForEach-Object {
        if ($_ -match "^GEMINI_API_KEY=(.+)$") {
            $ApiKey = $matches[1].Trim()
        }
    }
}

# Read HF Token from ple/.env if exists
$HfToken = ""
$PleEnvPath = Join-Path (Split-Path $PSScriptRoot -Parent) "ple\.env"
if (Test-Path $PleEnvPath) {
    Get-Content $PleEnvPath | ForEach-Object {
        if ($_ -match "^HF_TOKEN=(.+)$") {
            $HfToken = $matches[1].Trim()
        }
    }
}

if (-not $ApiKey) {
    Write-Error "ERROR: GEMINI_API_KEY not found in .env. Please check $EnvPath"
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 Launching PLE Batch 29-Task On-Demand VM (Option A)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "VM Name     : $InstanceName"
Write-Host "Zone        : $Zone"
Write-Host "Model / Type: $MachineType (Standard On-Demand, ~4.70 THB/hr, Zero Preemption)"
Write-Host "Tasks       : All 29 Tasks (Sequential Execution)"
Write-Host "Max Timeout : 6 Hours per task (Hard Limit)"
Write-Host "Watchdog    : 29 Hours OS-level auto-shutdown"
Write-Host "Canary Probe: AI Studio Credit exhaustion auto-shutdown"
Write-Host "Results GCS : $Bucket/runs/"
Write-Host "==========================================================" -ForegroundColor Cyan

$Metadata = "gcs-bucket=$Bucket,gemini-api-key=$ApiKey"
if ($HfToken) {
    $Metadata += ",hf-token=$HfToken"
}

gcloud compute instances create $InstanceName `
    --zone=$Zone `
    --machine-type=$MachineType `
    --boot-disk-type=pd-ssd `
    --boot-disk-size=100GB `
    --scopes=cloud-platform `
    --metadata=$Metadata `
    --metadata-from-file="startup-script=$StartupScript"

Write-Host "`n✅ On-Demand VM '$InstanceName' has been created successfully!" -ForegroundColor Green
Write-Host "💡 All 29 tasks are running sequentially. Monitor live logs with:" -ForegroundColor Yellow
Write-Host "gcloud compute instances get-serial-port-output $InstanceName --zone=$Zone --follow" -ForegroundColor Cyan

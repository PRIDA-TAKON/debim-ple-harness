param (
    [string]$TaskName = "footing-settlement-verification",
    [string]$Zone = "us-central1-a",
    [string]$Bucket = "gs://lab-ai-972593-ple-results"
)

$InstanceName = "ple-runner-$(Get-Date -Format 'MMdd-HHmm')"
$StartupScript = Join-Path $PSScriptRoot "scripts\gcp_spot_startup.sh"

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
Write-Host "🚀 Launching PLE Spot VM on Google Cloud Platform" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "VM Name     : $InstanceName"
Write-Host "Zone        : $Zone"
Write-Host "Model / Type: e2-standard-2 (Spot VM, ~0.50 THB/hr)"
Write-Host "Task Name   : $TaskName"
Write-Host "Results GCS : $Bucket/$TaskName"
Write-Host "Auto-Delete : Enabled (Max 6 hours or upon completion)"
Write-Host "==========================================================" -ForegroundColor Cyan

$Metadata = "task-name=$TaskName,gcs-bucket=$Bucket,gemini-api-key=$ApiKey"
if ($HfToken) {
    $Metadata += ",hf-token=$HfToken"
}

gcloud compute instances create $InstanceName `
    --zone=$Zone `
    --machine-type="e2-standard-2" `
    --boot-disk-size=50GB `
    --provisioning-model=SPOT `
    --instance-termination-action=DELETE `
    --max-run-duration=6h `
    --scopes=cloud-platform `
    --metadata=$Metadata `
    --metadata-from-file="startup-script=$StartupScript"

Write-Host "`n✅ VM '$InstanceName' has been created successfully!" -ForegroundColor Green
Write-Host "💡 The VM will run the task, upload output to $Bucket/$TaskName, and self-delete automatically." -ForegroundColor Yellow
Write-Host "To monitor live serial logs from your PC, run:" -ForegroundColor Cyan
Write-Host "gcloud compute instances get-serial-port-output $InstanceName --zone=$Zone --follow" -ForegroundColor White

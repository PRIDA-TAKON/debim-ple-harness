# ==============================================================================
# PowerShell Orchestrator: Deploy 4 Spot Workers in Multi-Zone GCP
# Working in tandem with ple-batch29-1121-1224 (Shard 2)
# ==============================================================================

$Project = "lab-ai-972593"
$StartupScript = "scripts/gcp_shard_runner.sh"
$Bucket = "gs://lab-ai-972593-ple-results/gemma4"

$Shards = @(
    @{
        Name = "ple-shard1"
        Zone = "us-central1-c"
        ShardId = "shard-1"
        Tasks = "fill-compaction-acceptance footing-settlement-verification division-26-specifications solar-supplemental-review permission-to-operate-memo pre-application-capacity-response"
    },
    @{
        Name = "ple-shard3"
        Zone = "us-central1-a"
        ShardId = "shard-3"
        Tasks = "heat-rejection-life-cycle-cost cooling-water-flush-plan wind-diaphragm-shear seismic-diaphragm-shear roof-deck-design data-hall-mep-routing"
    },
    @{
        Name = "ple-shard4"
        Zone = "us-central1-b"
        ShardId = "shard-4"
        Tasks = "data-hall-mep-routing-offset data-center-site-model fire-test-validation-memo fire-solve-convergence les-mesh-resolution eor-review-corrections"
    },
    @{
        Name = "ple-shard5"
        Zone = "us-central1-f"
        ShardId = "shard-5"
        Tasks = "foundation-strategy frame-extension-method mv-conveyance-study data-hall-device-takeoff shoring-design-verification"
    }
)

Write-Host "=========================================================="
Write-Host "Launching 4 Multi-Zone Spot Workers for PLE-Bench 29 Tasks"
Write-Host "Worker 2 (Shard 2: tasks 7-12) is already running on ple-batch29-1121-1224"
Write-Host "=========================================================="

foreach ($shard in $Shards) {
    $name = $shard.Name
    $zone = $shard.Zone
    $id = $shard.ShardId
    $tasks = $shard.Tasks
    
    Write-Host "Checking if $name exists in zone $zone..."
    $existing = gcloud compute instances list --filter="name=$name" --format="value(name)"
    if ($existing) {
        Write-Host "Instance $name already exists. Deleting to start fresh..."
        gcloud compute instances delete $name --zone=$zone --quiet
    }

    Write-Host "Launching Spot instance: $name (Zone: $zone, Tasks: $id)..."
    gcloud compute instances create $name `
        --project=$Project `
        --zone=$zone `
        --machine-type=e2-standard-4 `
        --provisioning-model=SPOT `
        --instance-termination-action=STOP `
        --boot-disk-size=80GB `
        --boot-disk-type=pd-ssd `
        --image-family=debian-12 `
        --image-project=debian-cloud `
        --scopes=cloud-platform `
        --metadata-from-file=startup-script=$StartupScript `
        --metadata="shard-id=$id,shard-tasks=$tasks,gcs-bucket=$Bucket,gemini-api-key=dummy-key"
        
    Write-Host "✅ $name launched successfully in $zone!"
}

Write-Host "=========================================================="
Write-Host "All Spot Workers dispatched successfully!"
Write-Host "Monitor all shards at: $Bucket"
Write-Host "=========================================================="

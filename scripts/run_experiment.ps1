param(
    [string]$Mode = "train",
    [string]$Config = "configs/experiment.json",
    [string]$DataDir = "data/raw",
    [string]$Output = "outputs/reports/final_metrics.csv",
    [int]$Epochs = 0
)

$arguments = @(
    "scripts/run_experiment.py",
    "--mode", $Mode,
    "--config", $Config,
    "--data-dir", $DataDir,
    "--output", $Output
)

if ($Epochs -gt 0) {
    $arguments += @("--epochs", "$Epochs")
}

python @arguments

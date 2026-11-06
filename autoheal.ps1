

# ==========================================
# AutoHealOps - Automatic Self-Healing
# ==========================================

$ContainerName = "autohealops-app-1"
$HealthUrl = "http://localhost:8000/health"
$RecoveryInProgress = $false
$LastStatus = ""

# Load Telegram credentials
$EnvData = @{}

if (-not (Test-Path ".env")) {
    Write-Host ".env file not found!" -ForegroundColor Red
    exit 1
}

Get-Content ".env" | ForEach-Object {
    if ($_ -match '^\s*([^#=]+?)\s*=\s*(.*?)\s*$') {
        $EnvData[$matches[1].Trim()] = $matches[2].Trim().Trim('"').Trim("'")
    }
}

$BotToken = $EnvData["TELEGRAM_BOT_TOKEN"]
$ChatId = $EnvData["TELEGRAM_CHAT_ID"]

if (-not $BotToken -or -not $ChatId) {
    Write-Host "Telegram credentials missing!" -ForegroundColor Red
    exit 1
}

# Telegram notification
function Send-TelegramMessage($Message) {
    try {
        $Url = "https://api.telegram.org/bot$BotToken/sendMessage"

        $Response = Invoke-RestMethod `
            -Uri $Url `
            -Method Post `
            -Body @{
                chat_id = $ChatId
                text = $Message
            } `
            -TimeoutSec 10

        if ($Response.ok) {
            Write-Host "Telegram notification sent." -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Telegram notification failed: $_" -ForegroundColor Red
    }
}

# Watchdog start
Write-Host "==================================" -ForegroundColor Cyan
Write-Host " AutoHealOps Watchdog Started " -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan

while ($true) {
    try {
        $Status = docker inspect --format='{{.State.Status}}' $ContainerName 2>$null

        if ($LASTEXITCODE -ne 0) {
            $Status = "missing"
        }

        $IsHealthy = $false

        if ($Status -eq "running") {
            try {
                $Health = docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $ContainerName 2>$null

                if ($Health -eq "healthy") {
                    $IsHealthy = $true
                }
                elseif ($Health -eq "none") {
                    $Response = Invoke-WebRequest `
                        -Uri $HealthUrl `
                        -TimeoutSec 5 `
                        -UseBasicParsing

                    if ($Response.StatusCode -eq 200) {
                        $IsHealthy = $true
                    }
                }
            }
            catch {
                $IsHealthy = $false
            }
        }

        if ($IsHealthy) {
            if ($RecoveryInProgress) {
                Write-Host "App recovered successfully!" -ForegroundColor Green
                Send-TelegramMessage "AutoHealOps RECOVERED: App is healthy again."
                $RecoveryInProgress = $false
            }

            if ($LastStatus -ne "healthy") {
                Write-Host "App Status: HEALTHY" -ForegroundColor Green
            }

            $LastStatus = "healthy"
        }
        else {
            Write-Host "App is unhealthy. Status: $Status" -ForegroundColor Red

            if (-not $RecoveryInProgress) {
                Send-TelegramMessage "AutoHealOps ALERT: App is unhealthy. Recovery started."
                $RecoveryInProgress = $true
            }

            if ($Status -eq "missing") {
                Write-Host "Container not found. Check Docker Compose." -ForegroundColor Red
            }
            else {
                Write-Host "Attempting container restart..." -ForegroundColor Yellow

                docker restart $ContainerName

                if ($LASTEXITCODE -eq 0) {
                    Write-Host "Recovery restart requested." -ForegroundColor Green
                }
                else {
                    Write-Host "Restart failed. Check Docker." -ForegroundColor Red
                }
            }

            $LastStatus = "unhealthy"
        }
    }
    catch {
        Write-Host "Watchdog error: $_" -ForegroundColor Red
    }

    Start-Sleep -Seconds 30
}
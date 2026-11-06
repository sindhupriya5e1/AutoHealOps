# AutoHealOps - Host-side Docker Compose watchdog
# Run this script from the repository root in PowerShell.

$HealthUrl = "http://localhost:8000/health"
$CheckIntervalSeconds = 30
$RecoveryInProgress = $false
$LastStatus = ""

# Telegram is optional. If .env exists, read credentials without printing them.
$BotToken = $env:TELEGRAM_BOT_TOKEN
$ChatId = $env:TELEGRAM_CHAT_ID
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#=]+?)\s*=\s*(.*?)\s*$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            if ($key -eq "TELEGRAM_BOT_TOKEN" -and -not $BotToken) { $BotToken = $value }
            if ($key -eq "TELEGRAM_CHAT_ID" -and -not $ChatId) { $ChatId = $value }
        }
    }
}

function Send-TelegramMessage([string]$Message) {
    if (-not $BotToken -or -not $ChatId) {
        Write-Host "Telegram not configured; skipping notification." -ForegroundColor DarkYellow
        return
    }
    try {
        $Url = "https://api.telegram.org/bot$BotToken/sendMessage"
        Invoke-RestMethod -Uri $Url -Method Post -Body @{ chat_id = $ChatId; text = $Message } -TimeoutSec 10 | Out-Null
        Write-Host "Telegram notification sent." -ForegroundColor Green
    }
    catch {
        Write-Host "Telegram notification failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AutoHealOps watchdog started" -ForegroundColor Green
Write-Host " Checking $HealthUrl every $CheckIntervalSeconds seconds"
Write-Host " Press Ctrl+C to stop"
Write-Host "========================================" -ForegroundColor Cyan

while ($true) {
    $IsHealthy = $false
    try {
        $Response = Invoke-WebRequest -Uri $HealthUrl -TimeoutSec 5 -UseBasicParsing
        $IsHealthy = ($Response.StatusCode -eq 200)
    }
    catch {
        $IsHealthy = $false
    }

    if ($IsHealthy) {
        if ($LastStatus -ne "healthy") {
            Write-Host "App status: HEALTHY" -ForegroundColor Green
        }
        if ($RecoveryInProgress) {
            Write-Host "App recovered successfully." -ForegroundColor Green
            Send-TelegramMessage "AutoHealOps RECOVERED: local app is healthy again."
            $RecoveryInProgress = $false
        }
        $LastStatus = "healthy"
    }
    else {
        Write-Host "App is unhealthy. Attempting Docker Compose recovery..." -ForegroundColor Red
        if (-not $RecoveryInProgress) {
            Send-TelegramMessage "AutoHealOps ALERT: local app is unhealthy. Recovery started."
            $RecoveryInProgress = $true
        }

        # 'up -d' starts the service if stopped and recreates it if required.
        docker compose up -d --no-deps app
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker Compose recovery command completed; health will be rechecked." -ForegroundColor Yellow
        }
        else {
            Write-Host "Recovery command failed. Check Docker Desktop and Compose." -ForegroundColor Red
        }
        $LastStatus = "unhealthy"
    }

    Start-Sleep -Seconds $CheckIntervalSeconds
}

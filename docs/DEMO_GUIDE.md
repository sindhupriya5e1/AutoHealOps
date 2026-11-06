# AutoHealOps Demo & Verification Guide

## Public demo
Open https://autohealops-demo.onrender.com/. The dashboard refreshes hosted API metrics every five seconds.

- /health — health response
- /api/metrics — current container resource metrics as JSON
- /metrics — Prometheus exposition
- /docs — interactive API documentation

## Full local demo
From the repository root, create a private .env file (Telegram credentials optional for the app, required to receive Telegram messages), then run:

    docker compose up -d --build
    docker compose ps

Open Grafana at http://localhost:3000 and configure the Prometheus data source URL as http://prometheus:9090. Open Prometheus at http://localhost:9090 and query:
- system_cpu_percent
- system_memory_percent
- system_disk_percent

Start the watchdog in a separate PowerShell window:

    .\autoheal.ps1

Controlled test:
1. Keep the watchdog running.
2. Run docker compose stop app in another terminal.
3. Wait up to 30 seconds for the watchdog to detect the stopped app.
4. The current script attempts docker restart autohealops-app-1. Check docker compose ps first; if the generated container name differs, update $ContainerName in autoheal.ps1 before testing.
5. Confirm http://localhost:8000/health returns a healthy response.
6. If configured, confirm Telegram receives unhealthy and recovered messages.

## Public-host limitation
Render hosts only the FastAPI dashboard/API. It does not host local Prometheus, Grafana or the host-side PowerShell watchdog. Public dashboard metrics belong to the Render container, not the user's laptop.

# AutoHealOps — Demo & Verification Guide

## 1. Public demo (reviewer flow)
Start here: https://autohealops-demo.onrender.com/

The main page displays hosted FastAPI CPU, memory and disk metrics and links to the public monitoring services.

- Health JSON: https://autohealops-demo.onrender.com/health
- JSON metrics: https://autohealops-demo.onrender.com/api/metrics
- Prometheus exposition: https://autohealops-demo.onrender.com/metrics
- Prometheus target status API: https://autohealops-demo.onrender.com/api/monitoring
- API docs: https://autohealops-demo.onrender.com/docs
- Prometheus UI: https://autohealops-prometheus-live.onrender.com/
- Prometheus targets: https://autohealops-prometheus-live.onrender.com/targets
- Grafana dashboard: https://autohealops-grafana-live.onrender.com/d/autohealops-live/autohealops-live?orgId=1&refresh=15s

Public Prometheus scrapes the hosted FastAPI `/metrics` endpoint. Grafana is configured with the hosted Prometheus service as its data source and provisions the AutoHealOps dashboard.

## 2. Local full-stack demo
Prerequisites: Docker Desktop/Engine, Docker Compose and PowerShell.

From the repository root:

```powershell
docker compose up -d --build
docker compose ps
```

Open:
- App dashboard: http://localhost:8000/
- Prometheus: http://localhost:9090/
- Grafana: http://localhost:3000/

Prometheus local scrape configuration is in `prometheus/prometheus.yml` and scrapes `app:8000` every 5 seconds. Grafana data source should point to `http://prometheus:9090` when configuring manually.

## 3. Demonstrate self-healing
Open a second PowerShell window at the repository root and run:

```powershell
.\autoheal.ps1
```

In another terminal, simulate an app failure:

```powershell
docker compose stop app
```

The watchdog checks the health endpoint every 30 seconds. When the health request fails, it attempts:

```powershell
docker compose up -d --no-deps app
```

Verify recovery:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8000/health
```

The watchdog discovers the Compose app service; it does not require a hard-coded container name. Telegram messages are optional and require `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in a private `.env` file or environment variables.

## 4. Important scope distinction
The public Render services demonstrate FastAPI metrics, Prometheus scraping and Grafana visualization for the hosted Render container. The PowerShell watchdog and Docker Compose recovery test run on the local project host. They do not restart the public Render service. Public cloud recovery is not included in this version.

Render free services may sleep after inactivity, and ephemeral service storage is not suitable for long-term metrics retention.

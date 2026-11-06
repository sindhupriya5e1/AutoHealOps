# AutoHealOps — Live DevOps Monitoring & Self-Healing Demo

**Author:** Sindhupriya Abbineni  
**Repository:** https://github.com/sindhupriya5e1/AutoHealOps

AutoHealOps is a containerized DevOps project that monitors CPU, memory and disk usage, exposes Prometheus metrics, visualizes them in Grafana, supports optional Telegram threshold alerts, and demonstrates local Docker Compose recovery using a PowerShell watchdog.

## Start the live demo

**[Open the AutoHealOps main dashboard](https://autohealops-demo.onrender.com/)**

The main page displays live metrics from the hosted FastAPI container and links to the monitoring services.

| Component | Public URL |
|---|---|
| Main dashboard | https://autohealops-demo.onrender.com/ |
| Health check | https://autohealops-demo.onrender.com/health |
| JSON metrics | https://autohealops-demo.onrender.com/api/metrics |
| Prometheus metrics | https://autohealops-demo.onrender.com/metrics |
| Prometheus status | https://autohealops-demo.onrender.com/api/monitoring |
| Prometheus UI | https://autohealops-prometheus-live.onrender.com/ |
| Prometheus targets | https://autohealops-prometheus-live.onrender.com/targets |
| Grafana dashboard | https://autohealops-grafana-live.onrender.com/d/autohealops-live/autohealops-live?orgId=1&refresh=15s |
| API documentation | https://autohealops-demo.onrender.com/docs |

## Features

- FastAPI dashboard and health endpoint.
- CPU, memory and disk metrics collected using psutil.
- Prometheus gauges: `system_cpu_percent`, `system_memory_percent`, `system_disk_percent`.
- Hosted Prometheus service scrapes the public FastAPI `/metrics` endpoint.
- Hosted Grafana is provisioned with a Prometheus data source and AutoHealOps resource dashboard.
- Optional Telegram alerts at CPU 80%, memory 80% and disk 85%.
- PowerShell watchdog checks the local app health every 30 seconds and attempts Docker Compose recovery.
- Docker Compose runs the local app, Prometheus and Grafana.

## Architecture

### Public monitoring demo
Browser → Render FastAPI dashboard/API → Prometheus scraper → Grafana dashboard.

### Local recovery demo
Docker Compose app → health endpoint → PowerShell watchdog → `docker compose up -d --no-deps app` when the health check fails. Telegram notifications are sent only when credentials are configured.

## Technology stack

| Technology | Purpose |
|---|---|
| Python 3.12, FastAPI, Uvicorn | API and dashboard |
| psutil | System resource measurements |
| prometheus-client | Metrics exposition |
| Prometheus | Scraping and querying |
| Grafana | Dashboards and visualization |
| Docker, Docker Compose | Containers and local orchestration |
| PowerShell | Local host watchdog and recovery |
| Telegram Bot API | Optional alerts |
| GitHub, Render | Source control and public demo hosting |

## Run the complete stack locally

### Prerequisites
- Docker Desktop with WSL integration enabled (Windows) or Docker Engine + Compose
- PowerShell 5.1+ / PowerShell 7+

### Start services
Clone the repository, open its root folder, then run:

```powershell
docker compose up -d --build
docker compose ps
```

Telegram is optional. To enable it, create a private `.env` file in the repository root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Never commit `.env` or share bot credentials.

### Open local services

| Component | Local URL |
|---|---|
| App dashboard | http://localhost:8000/ |
| Health | http://localhost:8000/health |
| JSON metrics | http://localhost:8000/api/metrics |
| Prometheus metrics | http://localhost:8000/metrics |
| Prometheus UI | http://localhost:9090/ |
| Grafana UI | http://localhost:3000/ |

Local Prometheus scrapes `app:8000` every 5 seconds using `prometheus/prometheus.yml`. If configuring Grafana manually, use `http://prometheus:9090` as the data source URL from inside the Grafana container.

### Run the watchdog and test recovery
In a separate PowerShell window from the repository root:

```powershell
.\autoheal.ps1
```

In another terminal, simulate an app failure:

```powershell
docker compose stop app
```

The watchdog checks every 30 seconds and attempts to bring the app back using Docker Compose. Verify:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8000/health
```

The watchdog discovers the Compose app service and does not rely on a fixed container name.

## Project submission documents and evidence

- [Project report](./docs/PROJECT_REPORT.md)
- [Demo and verification guide](./docs/DEMO_GUIDE.md)
- [Actual project evidence screenshots (PDF)](./AutoHealOps_Actual_Project_Evidence.pdf)
- [Architecture diagram (PDF)](./AutoHealOps_Architecture_Diagram.pdf)

## Deployment scope and limitations

- Public FastAPI, Prometheus and Grafana services are deployed separately on Render.
- The public Prometheus configuration scrapes the hosted FastAPI metrics endpoint; Grafana uses the hosted Prometheus data source.
- Public resource metrics describe the Render-hosted API container, not the developer's laptop.
- The PowerShell watchdog and Docker recovery workflow are local-host demonstrations. They do not restart the public Render service; public cloud self-healing is not implemented.
- Telegram alerts are optional and are skipped when credentials are not configured.
- Render free services may sleep after inactivity. Prometheus/Grafana data on ephemeral storage may be lost after service restarts. This is a portfolio demonstration, not a production monitoring platform.

## Conclusion
AutoHealOps demonstrates practical DevOps concepts: containerization, resource monitoring, metrics scraping, dashboard visualization, threshold alerting and local automated recovery. The public demo lets reviewers explore the dashboard and monitoring services, while the local setup demonstrates the self-healing workflow.

# AutoHealOps — Project Report

**Project title:** AutoHealOps — Automated DevOps Monitoring and Self-Healing Demo  
**Author:** Sindhupriya Abbineni  
**Repository:** https://github.com/sindhupriya5e1/AutoHealOps  
**Public dashboard:** https://autohealops-demo.onrender.com/

## Abstract
AutoHealOps is a containerized DevOps monitoring and recovery demonstration. A Python FastAPI application collects CPU, memory and disk utilization using psutil and exposes the values as Prometheus metrics. A Prometheus service scrapes the public API, and Grafana uses Prometheus as its data source to visualize resource usage. Optional Telegram notifications are sent when configured thresholds are crossed. A PowerShell watchdog runs on the local host, checks the local application health endpoint and attempts to restore the Docker Compose application when it becomes unavailable.

## Problem statement
Application downtime and high resource utilization can affect service availability. Developers need a way to observe resource usage, detect unhealthy application behavior, receive alerts and initiate recovery. This project demonstrates those practices in a small, reproducible environment.

## Objectives
- Monitor CPU, memory and disk utilization.
- Expose application metrics in Prometheus format.
- Scrape metrics using Prometheus.
- Visualize metrics using Grafana dashboards.
- Send optional Telegram alerts at configured thresholds.
- Check local application health using a PowerShell watchdog.
- Demonstrate recovery of a stopped or unhealthy local Docker Compose service.
- Provide public URLs for reviewers to inspect the API, Prometheus and Grafana.

## Technology stack
| Technology | Purpose |
|---|---|
| Python 3.12 | Application runtime |
| FastAPI + Uvicorn | Dashboard and REST API |
| psutil | CPU, memory and disk measurements |
| prometheus-client | Prometheus metric exposition |
| Prometheus | Metrics scraping and querying |
| Grafana | Metrics visualization |
| Docker + Docker Compose | Containerization and local orchestration |
| PowerShell | Host-side health watchdog and recovery |
| Telegram Bot API | Optional notifications |
| GitHub | Source control and project documentation |
| Render | Public demo hosting |

## Architecture
### Public monitoring demo
1. A reviewer opens the public FastAPI dashboard.
2. FastAPI collects resource metrics from the hosted application container.
3. Prometheus scrapes the FastAPI `/metrics` endpoint using the public scrape configuration.
4. Grafana reads the Prometheus data source and renders CPU, memory and disk panels.
5. The dashboard links to health, metrics, API documentation, Prometheus and Grafana.

### Local recovery demonstration
1. Docker Compose starts the FastAPI app, Prometheus and Grafana locally.
2. The PowerShell watchdog checks `http://localhost:8000/health` every 30 seconds.
3. If the endpoint fails, the watchdog runs `docker compose up -d --no-deps app`.
4. The watchdog checks health again and reports recovery.
5. Telegram failure/recovery notifications are sent only when bot credentials are configured.

## Main application endpoints
| Endpoint | Description |
|---|---|
| `/` | Live dashboard |
| `/health` | Health status JSON |
| `/api/info` | Project metadata and deployment scope |
| `/api/metrics` | Current CPU, memory and disk values as JSON |
| `/metrics` | Prometheus exposition format |
| `/api/monitoring` | Public Prometheus service and scrape-target status |
| `/docs` | FastAPI interactive API documentation |

## Metrics and alert thresholds
The application exposes:
- `system_cpu_percent`
- `system_memory_percent`
- `system_disk_percent`

Thresholds:
| Metric | Threshold |
|---|---:|
| CPU | 80% |
| Memory | 80% |
| Disk | 85% |

Telegram notifications are optional. The application logs a skipped-notification message if credentials are absent.

## Run locally
Prerequisites: Docker Desktop/Engine, Docker Compose and PowerShell.

1. Clone the repository.
2. Optional: create a private `.env` file with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to enable Telegram messages. Do not commit this file.
3. Run:
   ```powershell
   docker compose up -d --build
   docker compose ps
   ```
4. Open:
   - App: http://localhost:8000/
   - Prometheus: http://localhost:9090/
   - Grafana: http://localhost:3000/
5. In Grafana, configure Prometheus data source as `http://prometheus:9090` if provisioning is not used.
6. In a separate PowerShell window at the repository root, run:
   ```powershell
   .\autoheal.ps1
   ```
7. In another terminal, simulate failure:
   ```powershell
   docker compose stop app
   ```
8. Wait for the watchdog's next health check and verify:
   ```powershell
   docker compose ps
   Invoke-RestMethod http://localhost:8000/health
   ```

The watchdog uses Docker Compose service discovery and does not depend on a hard-coded container name. Telegram is optional.

## Public demo links
- Main dashboard: https://autohealops-demo.onrender.com/
- Health: https://autohealops-demo.onrender.com/health
- JSON metrics: https://autohealops-demo.onrender.com/api/metrics
- Prometheus metrics: https://autohealops-demo.onrender.com/metrics
- Prometheus UI: https://autohealops-prometheus-live.onrender.com/
- Prometheus targets: https://autohealops-prometheus-live.onrender.com/targets
- Grafana dashboard: https://autohealops-grafana-live.onrender.com/d/autohealops-live/autohealops-live?orgId=1&refresh=15s
- API documentation: https://autohealops-demo.onrender.com/docs

## Verification notes and limitations
- Render deployment logs confirmed the FastAPI service responds successfully to `GET /`, `GET /health` and repeated `GET /metrics` requests.
- Render deployment logs confirmed Prometheus and Grafana services started successfully. Grafana logs confirmed provisioning of the Prometheus data source and dashboard.
- The public metrics describe the Render-hosted FastAPI container, not the developer's laptop.
- The PowerShell watchdog recovers the local Docker Compose app only. It does not restart the public Render service. Public cloud self-healing is not implemented in this version.
- Telegram messages require a bot token and chat ID; without them, notifications are skipped.
- Render free services may sleep after inactivity. Data stored on ephemeral filesystems may be lost on restart. This is a portfolio/demo deployment, not a production monitoring service.

## Conclusion
AutoHealOps demonstrates application health checks, resource metrics collection, Prometheus scraping, Grafana visualization, optional alerting, Docker Compose orchestration and a local host-side recovery workflow. The public services allow reviewers to explore the monitoring interface, while the local setup demonstrates controlled self-healing behavior.

## Supporting evidence
See the repository's `AutoHealOps_Actual_Project_Evidence.pdf` and `AutoHealOps_Architecture_Diagram.pdf` for screenshots and the architecture overview.

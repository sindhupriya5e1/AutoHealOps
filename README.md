# AutoHealOps — Live DevOps Monitoring & Self-Healing Demo

**Built by Sindhupriya Abbineni** · [GitHub repository](https://github.com/sindhupriya5e1/AutoHealOps)

AutoHealOps is a containerized DevOps project that monitors CPU, memory and disk usage, exposes Prometheus metrics, visualizes them in Grafana, sends threshold alerts through Telegram, and uses a PowerShell watchdog to recover an unhealthy local application container.

## Live demo

**[Open AutoHealOps Live Dashboard](https://autohealops-demo.onrender.com/)**

- [Health check](https://autohealops-demo.onrender.com/health)
- [Live JSON metrics](https://autohealops-demo.onrender.com/api/metrics)
- [Prometheus exposition](https://autohealops-demo.onrender.com/metrics)
- [Interactive API documentation](https://autohealops-demo.onrender.com/docs)
- [Project information](https://autohealops-demo.onrender.com/api/info)

The public Render deployment hosts the FastAPI application and dashboard. The resource figures on the public page belong to the hosted container. The complete Prometheus + Grafana + Docker Compose + PowerShell watchdog recovery workflow runs locally. The public service cannot monitor or restart a personal laptop.

## Actual project evidence

The repository includes [AutoHealOps_Actual_Project_Evidence.pdf](./AutoHealOps_Actual_Project_Evidence.pdf), containing 10 screenshots from the running setup:
1. Grafana system dashboard (CPU, memory, disk, process memory and app health)
2. Prometheus CPU metric query
3. Prometheus memory metric query
4. Prometheus disk metric query
5. Docker Compose services and app health
6. FastAPI /health response
7. PowerShell watchdog startup
8. Controlled Docker container stop test
9. Watchdog recovery output
10. Telegram unhealthy/recovery notifications

See the [architecture diagram PDF](./AutoHealOps_Architecture_Diagram.pdf).

## Features

- FastAPI endpoints: /, /health, /api/info, /api/metrics, /metrics
- CPU, memory and disk monitoring through psutil
- Prometheus gauges: system_cpu_percent, system_memory_percent, system_disk_percent
- Prometheus scraping every 5 seconds and Grafana dashboards
- Telegram threshold alerts (CPU 80%, memory 80%, disk 85%)
- Host-side PowerShell watchdog checks health every 30 seconds
- Watchdog discovers the Compose app container dynamically and attempts recovery
- Public dashboard refreshes hosted API metrics every 5 seconds

## Architecture

    LOCAL DOCKER COMPOSE
    FastAPI + psutil -- /metrics --> Prometheus -- queries --> Grafana
          |                             
          +-- threshold alerts --> Telegram Bot
          ^
          | health checks / restart
    PowerShell watchdog -- docker compose restart app / up -d app

    PUBLIC PORTFOLIO DEMO
    Browser --> Render --> FastAPI dashboard + /health + /api/metrics + /metrics

## Technology stack

| Technology | Role |
|---|---|
| Python 3.12 | Application runtime |
| FastAPI + Uvicorn | API and dashboard server |
| psutil | CPU, memory and disk measurements |
| prometheus-client | Prometheus metric exposition |
| Prometheus | Local metrics scraping and storage |
| Grafana | Local dashboards and visualization |
| Docker + Docker Compose | Containerization and local orchestration |
| PowerShell | Host-side health watchdog and recovery |
| Telegram Bot API | Threshold, failure and recovery notifications |
| Render | Public FastAPI demo hosting |
| GitHub | Source control and documentation |

## Run the complete stack locally

### Prerequisites
- Docker Desktop with WSL integration enabled (Windows) or Docker Engine + Compose
- PowerShell 5.1+ / PowerShell 7+
- Telegram bot credentials if notifications are required

Create a private .env file in the repository root:

    TELEGRAM_BOT_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id

Keep .env private; it is excluded from Git. The app can run without Telegram credentials, but the current Compose file expects the .env file to exist.

### Start services

    docker compose up -d --build
    docker compose ps

Open:
| Component | Local URL |
|---|---|
| App dashboard | http://localhost:8000/ |
| Health | http://localhost:8000/health |
| JSON metrics | http://localhost:8000/api/metrics |
| Prometheus metrics | http://localhost:8000/metrics |
| Prometheus UI | http://localhost:9090 |
| Grafana UI | http://localhost:3000 |

Configure Grafana's Prometheus data source as http://prometheus:9090 from inside the Grafana container. Useful queries: system_cpu_percent, system_memory_percent, system_disk_percent.

### Start the watchdog

In a separate PowerShell window at the repository root:

    .\autoheal.ps1

The current watchdog script targets the Compose container name autohealops-app-1, checks http://localhost:8000/health every 30 seconds, and runs docker restart autohealops-app-1 when the app is unhealthy. Confirm the actual name with docker compose ps and update $ContainerName in autoheal.ps1 if your Compose project generates a different name. The current script requires a .env file with Telegram bot token and chat ID.

### Controlled recovery test

1. Confirm docker compose ps shows the app healthy.
2. Start .\autoheal.ps1 in PowerShell.
3. In another terminal run docker compose stop app.
4. Wait for the watchdog's next check (up to 30 seconds).
5. Confirm it attempts recovery and then reports healthy after the next successful health check.
6. Check Telegram for unhealthy and recovered messages if configured.

Perform this controlled test only in the local demo environment.

## Alert thresholds

| Metric | Threshold |
|---|---:|
| CPU | 80% |
| Memory | 80% |
| Disk | 85% |

An alert is sent when a metric first crosses its threshold. It can alert again after the value falls below the threshold and crosses again.

## Deployment notes and limitations

- Render hosts the FastAPI dashboard/API only. Public /metrics exposes metrics for the Render container.
- Prometheus, Grafana and the PowerShell watchdog remain part of the local Compose setup.
- Render free instances may spin down after inactivity and may restart. This is a portfolio demo, not production-grade monitoring.
- The host watchdog cannot restart the remote Render service.
- The current Compose file does not persist Prometheus or Grafana data.

## Project evidence and source

- [Actual project evidence screenshots (PDF)](./AutoHealOps_Actual_Project_Evidence.pdf)
- [Architecture diagram (PDF)](./AutoHealOps_Architecture_Diagram.pdf)
- [Project report](./docs/PROJECT_REPORT.md)
- [Demo verification guide](./docs/DEMO_GUIDE.md)
- [FastAPI application](./app/main.py)
- [PowerShell watchdog](./autoheal.ps1)
- [Prometheus config](./prometheus/prometheus.yml)

## Security

Never commit Telegram tokens, chat IDs, passwords or .env. Use authentication, secure secrets and persistent storage before adapting this learning demo for production.

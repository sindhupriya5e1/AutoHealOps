AutoHealOps – Automated DevOps Monitoring \& Self-Healing



AutoHealOps is a containerized DevOps monitoring and automatic recovery

project built using Python, Docker, Prometheus, Grafana and PowerShell.



\## Features



\- Real-time CPU, memory and disk monitoring

\- Prometheus metrics collection

\- Grafana monitoring dashboard

\- Application health monitoring

\- Automatic Docker container restart

\- Telegram failure and recovery notifications

\- Watchdog-based health checks



\## Technology Stack



\- Python

\- FastAPI

\- Docker and Docker Compose

\- Prometheus

\- Grafana

\- PowerShell

\- Telegram Bot API



\## Project Architecture



FastAPI Application → Prometheus → Grafana



PowerShell Watchdog → Docker Container Recovery → Telegram Alerts



\## Run the Project



Start the monitoring services:



```bash

docker compose up -d --build





Check container status:

docker compose ps





Start the automatic recovery watchdog in PowerShell:

.\\autoheal.ps1





Access Services

\- FastAPI: http://localhost:8000

\- Health Check: http://localhost:8000/health

\- Metrics: http://localhost:8000/metrics

\- Prometheus: http://localhost:9090

\- Grafana: http://localhost:3000

Automatic Recovery

The PowerShell watchdog monitors the application container.

When the container stops or becomes unhealthy, it attempts recovery

and sends Telegram notifications.

Security

Telegram credentials are stored in .env.

The .env file is excluded from Git using .gitignore.

Author

A.sindhupriya


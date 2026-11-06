# AutoHealOps — Project Report

**Project title:** AutoHealOps — Automated DevOps Monitoring and Self-Healing  
**Author:** Sindhupriya Abbineni  
**Repository:** https://github.com/sindhupriya5e1/AutoHealOps  
**Public demo:** https://autohealops-demo.onrender.com/

## Abstract
AutoHealOps demonstrates a practical DevOps observability and recovery workflow. A Python FastAPI service collects CPU, memory and disk utilization using psutil and exposes Prometheus metrics. Prometheus scrapes the application, Grafana visualizes the metrics, and Telegram can notify an operator when configured thresholds are crossed. A PowerShell watchdog runs on the host, checks the local application's health endpoint and attempts to recover the Docker Compose app container when it becomes unhealthy or stopped.

## Problem statement
Application interruptions and resource pressure can affect availability. Operators need visibility into resource usage and a repeatable way to detect failure and initiate recovery. AutoHealOps combines monitoring, alerting and a self-healing demonstration.

## Objectives
- Measure CPU, memory and disk usage.
- Expose metrics in Prometheus format.
- Collect and visualize metrics using Prometheus and Grafana.
- Send Telegram notifications when configured thresholds are crossed.
- Check application health from a host-side watchdog.
- Demonstrate a controlled container-stop and recovery scenario.
- Publish a public FastAPI dashboard/API for portfolio review.

## Technology stack
Python 3.12, FastAPI, Uvicorn, psutil, prometheus-client, requests, python-dotenv, Docker, Docker Compose, Prometheus, Grafana, PowerShell, Telegram Bot API, GitHub and Render.

## Architecture and workflow
1. FastAPI serves the dashboard, health endpoint and metrics endpoints.
2. psutil reads CPU, memory and disk utilization.
3. The application updates Prometheus gauges and checks thresholds.
4. Prometheus scrapes the app's /metrics endpoint every five seconds.
5. Grafana queries Prometheus and displays monitoring panels.
6. Telegram receives threshold notifications when bot credentials are configured.
7. The PowerShell watchdog checks the local app health endpoint every 30 seconds.
8. When the app is stopped or unhealthy, the watchdog attempts Docker Compose recovery and sends failure/recovery notifications when configured.

## Main endpoints
| Endpoint | Purpose |
|---|---|
| / | Live dashboard |
| /health | Application health response |
| /api/info | Project metadata and deployment scope |
| /api/metrics | Current CPU, memory and disk values as JSON |
| /metrics | Prometheus exposition format |
| /docs | FastAPI interactive API documentation |

## Alert thresholds
CPU 80%, memory 80%, disk 85%. The application avoids repeated notifications while a metric remains above its threshold and can alert again after it falls below and crosses again.

## Local setup
1. Install Docker Desktop/Engine and Docker Compose.
2. Clone the repository.
3. Create a private .env with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID if Telegram alerts are required.
4. Run docker compose up -d --build.
5. Open the app at http://localhost:8000, Prometheus at http://localhost:9090 and Grafana at http://localhost:3000.
6. Configure Grafana's Prometheus data source as http://prometheus:9090.
7. Run .\autoheal.ps1 in a separate PowerShell window.
8. Test recovery with docker compose stop app, then verify the watchdog attempts to restore the service.

## Actual project evidence supplied
The repository's AutoHealOps_Actual_Project_Evidence.pdf contains ten screenshots from the supplied running setup: Grafana dashboard; Prometheus CPU, memory and disk graphs; Docker Compose service status; app health endpoint; watchdog startup; container stop test; automatic recovery output; and Telegram failure/recovery notifications.

The evidence PDF also shows an initial PowerShell command-not-found error before later watchdog output. The current watchdog script uses a configured container name (autohealops-app-1). Confirm the name shown by docker compose ps and keep $ContainerName in autoheal.ps1 aligned with it. The supplied screenshot shows a command-not-found attempt before the later watchdog output; repeat the test from the repository folder to capture a clean run.

## Public live demo and scope
The public Render deployment hosts the FastAPI dashboard and API. It displays metrics collected from the hosted Render container. Prometheus, Grafana, Docker Compose orchestration and the PowerShell watchdog remain in the local setup. The watchdog operates on the local host and cannot restart the remote Render service.

## Conclusion
AutoHealOps combines containerization, resource monitoring, metrics collection, dashboards, threshold notifications, health checks and automated recovery attempts. It provides a public API/dashboard for portfolio demonstration and a local multi-container environment for the complete monitoring and recovery workflow.

## Links
- Live dashboard: https://autohealops-demo.onrender.com/
- Health: https://autohealops-demo.onrender.com/health
- JSON metrics: https://autohealops-demo.onrender.com/api/metrics
- Prometheus metrics: https://autohealops-demo.onrender.com/metrics
- API docs: https://autohealops-demo.onrender.com/docs
- Actual evidence PDF: https://github.com/sindhupriya5e1/AutoHealOps/blob/main/AutoHealOps_Actual_Project_Evidence.pdf

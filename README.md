# AutoHealOps – Automated DevOps Monitoring & Self-Healing

AutoHealOps is a containerized DevOps monitoring and recovery project. It exposes system resource metrics through a FastAPI application, collects them with Prometheus, visualizes them in Grafana, sends threshold alerts through Telegram, and uses a PowerShell watchdog to restart an unhealthy application container.

> **Scope:** This project demonstrates monitoring and recovery for the Dockerized application container. The watchdog must be running separately on the host in PowerShell.

## Features

- Monitors CPU, memory, and disk usage using `psutil`
- Exposes Prometheus-compatible metrics at `/metrics`
- Collects metrics with Prometheus
- Provides a Grafana interface for dashboards and visualization
- Provides application root and health-check endpoints
- Sends Telegram alerts when CPU, memory, or disk usage crosses configured thresholds
- Uses a PowerShell watchdog to check application health and attempt a Docker container restart
- Sends Telegram notifications when the watchdog detects a failure and when the application recovers

## Architecture

```text
                         +----------------------+
                         |     Grafana          |
                         |   localhost:3000     |
                         +----------+-----------+
                                    |
                                    | queries
                                    v
+------------------+      scrape   +----------------------+
| FastAPI app      | <-------------| Prometheus           |
| /health          |               | localhost:9090       |
| /metrics         |               +----------------------+
| CPU / Memory /   |
| Disk metrics     |------ threshold alerts ------> Telegram Bot
+--------+---------+
         ^
         | health check / Docker restart
         |
+--------+---------+
| PowerShell       |
| autoheal.ps1     |
| Watchdog         |
+------------------+
```

## Technology Stack

| Component | Purpose |
|---|---|
| Python | Monitoring application |
| FastAPI | HTTP API and health endpoint |
| psutil | CPU, memory, and disk metrics |
| Prometheus Client | Exposes application metrics |
| Docker | Containerizes the application |
| Docker Compose | Runs the application, Prometheus, and Grafana |
| Prometheus | Scrapes and stores metrics |
| Grafana | Metrics visualization |
| PowerShell | Watchdog and container restart logic |
| Telegram Bot API | Failure, recovery, and threshold notifications |

## Project Structure

```text
AutoHealOps/
├── app/
│   └── main.py
├── prometheus/
│   └── prometheus.yml
├── autoheal.ps1
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

Install the following on your machine:

- Docker Desktop (or Docker Engine) with the Docker Compose plugin
- PowerShell 5.1 or later (or PowerShell 7+)
- A Telegram account and a Telegram bot if you want to receive notifications

Check the installations:

```bash
docker --version
docker compose version
```

In PowerShell, check:

```powershell
$PSVersionTable.PSVersion
```

## Configuration

The Compose configuration expects a local `.env` file. Create it from the example:

**PowerShell**
```powershell
Copy-Item .env.example .env
```

**Linux / macOS**
```bash
cp .env.example .env
```

Add your Telegram credentials to `.env`:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Keep the real `.env` file private. It is excluded from Git by `.gitignore`; never commit bot tokens or other secrets. The application still runs without Telegram credentials, but Telegram notifications will not be sent.

## Run the Project

Run these commands from the repository root:

1. Build the application image and start all services:

   ```bash
   docker compose up -d --build
   ```

2. Check service status:

   ```bash
   docker compose ps
   ```

3. View application logs:

   ```bash
   docker compose logs -f app
   ```

4. Open the service endpoints:

   | Service | URL |
   |---|---|
   | FastAPI home | http://localhost:8000/ |
   | Health check | http://localhost:8000/health |
   | Prometheus metrics | http://localhost:8000/metrics |
   | Prometheus UI | http://localhost:9090 |
   | Grafana UI | http://localhost:3000 |

   Grafana's default initial login is commonly `admin` / `admin`; change the password when prompted. If the instance has already been configured, use the password set for that Grafana instance.

## Configure Grafana

1. Open http://localhost:3000 and sign in.
2. Add Prometheus as a data source.
3. Set the Prometheus server URL to `http://prometheus:9090` (the Compose service name is reachable from the Grafana container).
4. Save and test the data source.
5. Create a dashboard and add queries such as:

   - CPU usage: `system_cpu_percent`
   - Memory usage: `system_memory_percent`
   - Disk usage: `system_disk_percent`

The Prometheus scrape configuration is in `prometheus/prometheus.yml`; it scrapes the application at `app:8000` every 5 seconds.

## Start the Self-Healing Watchdog

The watchdog is a separate host-side PowerShell process; it is not started by Docker Compose.

1. Make sure the Compose services are running.
2. Open PowerShell in the repository root.
3. Run:

   ```powershell
   .\autoheal.ps1
   ```

The script checks the application container and its health every 30 seconds. If the container is unhealthy or stopped, it attempts to restart it with Docker and sends a Telegram alert. When it detects recovery, it sends a recovery notification.

**Important:** The script currently targets the Compose container name `autohealops-app-1`. If your Compose project uses a different project name or container name, update the `$ContainerName` value in `autoheal.ps1` to match the name shown by `docker compose ps`. Keep the watchdog PowerShell window running while you want recovery checks to continue.

## Alert Thresholds

The application sends a Telegram alert when a metric crosses its threshold:

| Metric | Threshold |
|---|---:|
| CPU usage | 80% |
| Memory usage | 80% |
| Disk usage | 85% |

Thresholds are defined in `app/main.py`. The application avoids repeatedly sending the same alert while a metric remains above its threshold; it can send a new alert after the metric returns below the threshold and crosses it again.

## Stop the Project

Stop and remove the Compose containers:

```bash
docker compose down
```

To also remove the Prometheus container's stored data, remove its data volume if you have configured one separately. The current Compose file does not define a persistent Prometheus or Grafana data volume, so container recreation can reset their stored state and Grafana configuration.

## Troubleshooting

- **Compose cannot find `.env`:** Create it by copying `.env.example` to `.env`.
- **A port is already in use:** Stop the process using port 8000, 9090, or 3000, or change the corresponding host port in `docker-compose.yml`.
- **Prometheus cannot scrape the app:** Check `docker compose ps`, `docker compose logs app`, and that the Prometheus target is configured as `app:8000`.
- **Telegram notifications do not arrive:** Verify the bot token and chat ID in your local `.env` file and confirm that you have started a conversation with the bot.
- **The watchdog cannot find the container:** Run `docker compose ps` and make sure `$ContainerName` in `autoheal.ps1` matches the actual application container name.

## Security Notes

- Do not commit `.env` or publish Telegram bot tokens.
- Use a unique, secure Grafana password.
- For a production deployment, add authentication, TLS, persistent storage, resource limits, and managed secret handling.

## Author

**Sindhupriya Abbineni**

GitHub: [@sindhupriya5e1](https://github.com/sindhupriya5e1)

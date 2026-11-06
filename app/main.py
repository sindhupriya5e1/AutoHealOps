from datetime import datetime
from pathlib import Path
import os

import psutil
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest

load_dotenv()
app = FastAPI(title="AutoHealOps", description="DevOps monitoring, alerting and self-healing demo", version="1.1.0")

cpu_metric = Gauge("system_cpu_percent", "CPU usage percentage")
memory_metric = Gauge("system_memory_percent", "Memory usage percentage")
disk_metric = Gauge("system_disk_percent", "Disk usage percentage")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CPU_THRESHOLD, MEMORY_THRESHOLD, DISK_THRESHOLD = 80, 80, 85
alert_states = {"CPU": False, "Memory": False, "Disk": False}


def send_telegram_alert(metric: str, value: float, threshold: int) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured; alert skipped.")
        return
    message = (
        f"AutoHealOps Alert!\nMetric: {metric}\nCurrent Usage: {value}%\n"
        f"Threshold: {threshold}%\nStatus: WARNING\nTime: {datetime.now().astimezone().isoformat()}"
    )
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=5,
        )
        response.raise_for_status()
        print(f"Telegram {metric} alert sent successfully.")
    except requests.RequestException as error:
        print(f"Telegram alert failed: {error}")


def check_alert(metric: str, value: float, threshold: int) -> None:
    is_high = value >= threshold
    if is_high and not alert_states[metric]:
        send_telegram_alert(metric, value, threshold)
    alert_states[metric] = is_high


def collect_metrics() -> dict:
    cpu = psutil.cpu_percent(interval=0.2)
    memory = round(psutil.virtual_memory().percent, 2)
    disk = round(psutil.disk_usage("/").percent, 2)
    cpu_metric.set(cpu)
    memory_metric.set(memory)
    disk_metric.set(disk)
    check_alert("CPU", cpu, CPU_THRESHOLD)
    check_alert("Memory", memory, MEMORY_THRESHOLD)
    check_alert("Disk", disk, DISK_THRESHOLD)
    return {
        "cpu_percent": cpu,
        "memory_percent": memory,
        "disk_percent": disk,
        "thresholds": {"cpu": CPU_THRESHOLD, "memory": MEMORY_THRESHOLD, "disk": DISK_THRESHOLD},
        "timestamp": datetime.now().astimezone().isoformat(),
    }


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard():
    page = Path(__file__).with_name("dashboard.html")
    return HTMLResponse(page.read_text(encoding="utf-8"))


@app.get("/api/info")
def info():
    return {
        "project": "AutoHealOps",
        "status": "Running",
        "version": app.version,
        "components": ["FastAPI", "psutil", "Prometheus", "Grafana", "Docker Compose", "PowerShell Watchdog", "Telegram"],
        "scope": "Public demo: FastAPI metrics are scraped by hosted Prometheus and visualized in hosted Grafana. PowerShell watchdog and Docker recovery remain a local-host demonstration.",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().astimezone().isoformat()}


@app.get("/api/metrics")
def metrics_json():
    return collect_metrics()


@app.get("/metrics")
def prometheus_metrics():
    collect_metrics()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


from fastapi import FastAPI
from fastapi.responses import Response
from datetime import datetime
import psutil
import os
import requests
from dotenv import load_dotenv

from prometheus_client import (
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AutoHealOps",
    description="Intelligent DevOps Monitoring Platform",
    version="1.0.0"
)

# Prometheus metrics
cpu_metric = Gauge(
    "system_cpu_percent",
    "CPU usage percentage"
)

memory_metric = Gauge(
    "system_memory_percent",
    "Memory usage percentage"
)

disk_metric = Gauge(
    "system_disk_percent",
    "Disk usage percentage"
)

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Alert thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 85

# Prevent repeated alerts
alert_states = {
    "CPU": False,
    "Memory": False,
    "Disk": False
}


# Send Telegram notification
def send_telegram_alert(metric, value, threshold):

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing")
        return

    message = (
        f"🚨 AutoHealOps Alert!\n\n"
        f"Metric: {metric}\n"
        f"Current Usage: {value}%\n"
        f"Threshold: {threshold}%\n"
        f"Status: WARNING\n"
        f"Time: {datetime.now().isoformat()}"
    )

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=5
        )

        response.raise_for_status()

        result = response.json()

        if result.get("ok"):
            print(f"Telegram {metric} alert sent successfully")
        else:
            print("Telegram API returned an error:", result)

    except requests.RequestException as error:
        print("Telegram alert failed:", error)


# Check threshold
def check_alert(metric, value, threshold):

    is_high = value >= threshold
    was_high = alert_states.get(metric, False)

    if is_high and not was_high:
        send_telegram_alert(metric, value, threshold)

    alert_states[metric] = is_high


# Home endpoint
@app.get("/")
def home():

    return {
        "project": "AutoHealOps",
        "status": "Running",
        "message": "DevOps Monitoring Platform is Online"
    }


# Health endpoint
@app.get("/health")
def health():

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


# Monitoring endpoint
@app.get("/metrics")
def metrics():

    # CPU usage
    cpu = psutil.cpu_percent(interval=1)

    # Memory usage
    mem = psutil.virtual_memory()

    memory = round(
        ((mem.total - mem.available) / mem.total) * 100,
        2
    )

    # Disk usage inside Docker container
    disk = psutil.disk_usage("/").percent

    # Update Prometheus metrics
    cpu_metric.set(cpu)
    memory_metric.set(memory)
    disk_metric.set(disk)

    # Check alerts
    check_alert("CPU", cpu, CPU_THRESHOLD)
    check_alert("Memory", memory, MEMORY_THRESHOLD)
    check_alert("Disk", disk, DISK_THRESHOLD)

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
)
    
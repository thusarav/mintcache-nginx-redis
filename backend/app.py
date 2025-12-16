from fastapi import FastAPI
import time
import psutil
import platform

app = FastAPI()

@app.get("/slow")
def slow():
    time.sleep(2)
    return {"message": "Slow response"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/mint-health")
def mint_health():
    return {
        "os": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
            "used_gb": round(psutil.disk_usage("/").used / (1024**3), 2),
            "percent": psutil.disk_usage("/").percent
        },
        "uptime_seconds": int(time.time() - psutil.boot_time())
    }

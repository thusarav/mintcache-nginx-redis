from fastapi import FastAPI, Request, HTTPException
import redis
import time
import psutil
import platform

# --------------------
# App setup
# --------------------
app = FastAPI()

# --------------------
# Redis client
# --------------------
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# --------------------
# Rate limit config
# --------------------
RATE_LIMIT = 5          # requests
WINDOW_SECONDS = 10     # per 10 seconds


def is_rate_limited(client_ip: str) -> bool:
    key = f"rate:{client_ip}"

    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, WINDOW_SECONDS)

    return current > RATE_LIMIT


# --------------------
# Public endpoints
# --------------------
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


# --------------------
# Internal rate-check endpoint (Nginx only)
# --------------------
@app.get("/_internal/rate-check")
def rate_check(request: Request):
    client_ip = request.client.host

    if is_rate_limited(client_ip):
        # auth_request ONLY understands 401/403
        raise HTTPException(status_code=403, detail="Rate limit exceeded")

    return {"status": "ok"}

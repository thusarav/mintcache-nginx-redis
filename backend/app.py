from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/slow")
def slow():
    time.sleep(2)
    return {"message": "Slow response"}

@app.get("/health")
def health():
    return {"status": "ok"}

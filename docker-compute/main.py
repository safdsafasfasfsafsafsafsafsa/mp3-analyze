# docker-compute/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI running inside Docker"}

@app.post("/analyze")
def analyze(data: dict):
    # 여기에 matplotlib, numpy 등 무거운 계산 수행
    return {"result": "processed"}

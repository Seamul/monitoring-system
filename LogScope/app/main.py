from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


# Auto Prometheus instrumentation
Instrumentator().instrument(app).expose(app)
from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from starlette.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST

app = FastAPI()

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    return response

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

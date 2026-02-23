

# Centralized Application Monitoring System

## FastAPI + Django + Prometheus + Grafana

This project provides a **centralized monitoring platform** for multiple backend services using:

* **Prometheus** → Metrics collection & storage
* **Grafana** → Visualization dashboards
* **Node Exporter** → Server resource monitoring
* **FastAPI** → Application metrics
* **Django** → Application metrics

---

#  Architecture Overview

```
                ┌──────────────┐
                │   FastAPI     │
                │   /metrics    │
                └──────┬───────┘
                       │
                ┌──────▼───────┐
                │    Django     │
                │   /metrics    │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  Prometheus  │
                │  Scraping    │
                └──────┬───────┘
                       ▼
                ┌──────────────┐
                │   Grafana    │
                │ Dashboards   │
                └──────────────┘

        Node Exporter → CPU / RAM / Disk Metrics
```

---

#  Monitoring Components

| Service       | Purpose                      |
| ------------- | ---------------------------- |
| FastAPI       | Application metrics exposure |
| Django        | Application metrics exposure |
| Prometheus    | Metrics collection & storage |
| Grafana       | Dashboard visualization      |
| Node Exporter | Server resource monitoring   |

---

# ⚡ Monitored Metrics

## Application Metrics

 Total API Requests
 Endpoint-wise Requests
 HTTP Method Usage
 Request Rate

## System Metrics

CPU Usage
Memory Usage
Disk Usage
Network Usage

---

#  FastAPI Metrics Implementation

## `main.py`

```python
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
    return Response(generate_latest(),
                    media_type=CONTENT_TYPE_LATEST)
```

### Metrics Endpoint

```
http://SERVER_IP:8000/metrics
```

---

# Django Metrics Implementation

Monitoring is enabled using:

**django-prometheus**

---

## Install

```bash
pip install django-prometheus
```

---

## settings.py

### Installed Apps

```python
INSTALLED_APPS = [
    "django_prometheus",
    ...
]
```

---

### Middleware

```python
MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    ...
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]
```

---

### Database Backend

```python
DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

---

## urls.py

```python
urlpatterns = [
    path("", include("django_prometheus.urls")),
]
```

---

### Metrics Endpoint

```
http://SERVER_IP:8009/metrics
```

---

# Prometheus Configuration

## `prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:

  - job_name: 'fastapi'
    metrics_path: /metrics
    static_configs:
      - targets:
          - 172.16.5.7:8000

  - job_name: 'django'
    metrics_path: /metrics
    static_configs:
      - targets:
          - 172.16.5.7:8009

  - job_name: 'node_exporter'
    static_configs:
      - targets:
          - 172.16.5.7:9100
```

---

# 🐳 Monitoring Server Stack

## docker-compose.yml

Services included:

Prometheus
Grafana
Persistent Storage

Start monitoring:

```bash
docker compose up -d
```

---

# 🌐 Service Access

| Service    | URL                   |
| ---------- | --------------------- |
| FastAPI    | http://SERVER_IP:8000 |
| Django     | http://SERVER_IP:8009 |
| Prometheus | http://SERVER_IP:9090 |
| Grafana    | http://SERVER_IP:3000 |

---

# Grafana Setup

## Login

```
Username: admin
Password: admin
```

---

## Add Prometheus Data Source

```
Settings → Data Sources → Add Prometheus
```

URL:

```
http://prometheus:9090
```

Click **Save & Test**

---

# Useful Prometheus Queries

## Total Requests

```
sum(app_requests_total)
```

---

## Requests Per Endpoint

```
sum by (endpoint)(app_requests_total)
```

---

## Requests Per Method

```
sum by (method)(app_requests_total)
```

---

## Requests Per Second

```
rate(app_requests_total[1m])
```

---

## Django Request Rate

```
rate(django_http_requests_total_by_method_total[1m])
```

---

# Generate Test Traffic

FastAPI:

```bash
curl http://SERVER_IP:8000/
```

Django:

```bash
curl http://SERVER_IP:8009/home/
```

---

# 🗄 Data Storage

Prometheus TSDB retention:

```bash
--storage.tsdb.retention.time=60d
```

Stores metrics for **60 days**.

---

# Monitoring Result

You can now monitor:

✔ FastAPI APIs
✔ Django APIs
✔ Server resources
✔ Traffic spikes
✔ Endpoint popularity
✔ Historical performance

---

# Production Recommendations

Recommended dashboards:

* API Requests/sec
* Error Rate
* Response Time
* CPU Usage
* Memory Usage
* Disk Usage
* Container Monitoring

---

# System Status

Your platform now supports:

 Multi-service monitoring
 Centralized observability
 Historical metrics
 Real-time dashboards
 Production-ready monitoring

---

**Ready-to-use Prometheus + Grafana queries**.

I’ll update only the **correct section** of the README by adding a new part:

FastAPI Queries
Django Queries
Recommended Grafana Panels
Production Monitoring Commands

Below is the **UPDATED README ADDITION** you should insert after **Grafana Setup / Useful Queries** section.

---

# Application Monitoring Queries (FastAPI + Django)

This section provides **ready-to-use Prometheus queries** for Grafana dashboards.

---

# FastAPI Monitoring Queries

FastAPI exposes custom metric:

```
app_requests_total
```

---

## 1. Total FastAPI Requests (Since Start)

```promql
sum(app_requests_total{job="fastapi"})
```

 Shows total requests handled since application startup.

**Grafana Panel**

*  Stat
*  Time Series

---

##  2. FastAPI Requests Per Second (Live Traffic)

```promql
sum(rate(app_requests_total{job="fastapi"}[1m]))
```

Shows:

* Requests/sec
* API load
* Live traffic

---

## 3. Requests Per Minute

```promql
sum(rate(app_requests_total{job="fastapi"}[1m])) * 60
```

Human-readable traffic monitoring.

---

##  4. Requests Per Endpoint

```promql
sum by (endpoint)(
  rate(app_requests_total{job="fastapi"}[1m])
)
```

Helps identify:

Most used APIs
Traffic hotspots

---

## 5. Requests By HTTP Method

```promql
sum by (method)(
  rate(app_requests_total{job="fastapi"}[1m])
)
```

Shows:

* GET
* POST
* PUT
* DELETE usage

---

# Django Monitoring Queries

Django metrics are automatically exposed via:

**django-prometheus**

Metric example:

```
django_http_requests_total_by_method_total
```

---

## 1. Django Total Requests (Since Start)

```promql
sum(django_http_requests_total_by_method_total{job="django"})
```

Displays total number of Django requests handled.

**Grafana Panel**

* Stat

---

## 2. Django Requests Per Second (Production Metric)

```promql
sum(
  rate(
    django_http_requests_total_by_method_total{
      job="django",
      view!="metrics"
    }[1m]
  )
)
```

Real-time traffic
Production monitoring
Excludes `/metrics` endpoint

---

##  3. Django Requests Per Minute

```promql
sum(
  rate(
    django_http_requests_total_by_method_total{
      job="django",
      view!="metrics"
    }[1m]
  )
) * 60
```

---

##  4. Requests By HTTP Method

```promql
rate(
  django_http_requests_total_by_method_total{
    job="django"
  }[1m]
)
```

Grafana automatically separates:

* GET
* POST
* PUT
* DELETE

---

##  5. Requests By Status Code  (Very Important)

```promql
sum by (status)(
  rate(
    django_http_responses_total_by_status_total{
      job="django"
    }[1m]
  )
)
```

Shows:

| Status | Meaning         |
| ------ | --------------- |
| 200    | Success       |
| 404    | Not Found     |
| 500    | Server Error  |

---

## 6. Django Error Rate (5xx Errors)

```promql
sum(
  rate(
    django_http_responses_total_by_status_total{
      status=~"5..",
      job="django"
    }[1m]
  )
)
```

Critical production monitoring metric.

---

# Recommended Grafana Dashboard Panels

---

## 🔹 Panel 1 — Total Requests

```promql
sum(django_http_requests_total_by_method_total{job="django"})
```

Panel Type →  **Stat**

---

## 🔹 Panel 2 — Requests/sec

```promql
sum(rate(django_http_requests_total_by_method_total{job="django"}[1m]))
```

Panel Type → **Time Series**

---

## 🔹 Panel 3 — Error Rate

```promql
sum(rate(django_http_responses_total_by_status_total{status=~"5..",job="django"}[1m]))
```

Panel Type → **Time Series**

---

## 🔹 Panel 4 — FastAPI Requests/sec

```promql
sum(rate(app_requests_total{job="fastapi"}[1m]))
```

---

#  Generate Test Traffic

Metrics appear **only after requests occur**.

---

### FastAPI

```bash
curl http://SERVER_IP:8000/
```

---

### Django

```bash
curl http://SERVER_IP:8009/home/
```

or refresh browser multiple times:

```
http://SERVER_IP:8009/home
```

---

# monitoring-system

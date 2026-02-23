

# 🚀 Centralized Application Monitoring System

## FastAPI + Django + Prometheus + Grafana

This project provides a **centralized monitoring platform** for multiple backend services using:

* **Prometheus** → Metrics collection & storage
* **Grafana** → Visualization dashboards
* **Node Exporter** → Server resource monitoring
* **FastAPI** → Application metrics (`prometheus-fastapi-instrumentator`)
* **Django** → Application metrics (`django-prometheus`)

---

# 🏗 Architecture Overview

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
                │  Prometheus   │
                │ Metrics Store │
                └──────┬────────┘
                       ▼
                ┌──────────────┐
                │   Grafana     │
                │ Dashboards    │
                └──────────────┘

        Node Exporter → CPU / Memory / Disk Metrics
```

---

# Monitoring Components

| Service       | Purpose                    |
| ------------- | -------------------------- |
| FastAPI       | API metrics exposure       |
| Django        | API metrics exposure       |
| Prometheus    | Metrics scraping & storage |
| Grafana       | Visualization dashboards   |
| Node Exporter | System monitoring          |

---

# ⚡ Monitored Metrics

## Application Metrics

 Total Requests
 Requests/sec
 Endpoint Usage
 HTTP Methods
 Status Codes
 API Latency

## System Metrics

 CPU Usage
 Memory Usage
 Disk Usage
 Network Usage

---

# ⚡ FastAPI Metrics Implementation

Monitoring enabled using:

 **prometheus-fastapi-instrumentator**

---

## Install

```bash
pip install prometheus-fastapi-instrumentator[metrics]
```

---

## `main.py`

```python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


# Automatic Prometheus metrics
Instrumentator().instrument(app).expose(app)
```

---

## FastAPI Metrics Endpoint

```
http://SERVER_IP:8000/metrics
```

Automatically exposes:

* request count
* latency
* status codes
* request duration
* in-progress requests

---

#  Django Metrics Implementation

Monitoring enabled using:

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

## Django Metrics Endpoint

```
http://SERVER_IP:8009/metrics
```

---

#  Prometheus Configuration

## `prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:

  - job_name: "fastapi"
    metrics_path: /metrics
    static_configs:
      - targets:
          - 172.16.5.7:8000

  - job_name: "django"
    metrics_path: /metrics
    static_configs:
      - targets:
          - 172.16.5.7:8009

  - job_name: "node_exporter"
    static_configs:
      - targets:
          - 172.16.5.7:9100
```

---

# 🐳 Central Monitoring Server

Start monitoring stack:

```bash
docker compose up -d
```

Includes:

 Prometheus
 Grafana
 Persistent volumes

---

# Service Access

| Service    | URL                   |
| ---------- | --------------------- |
| FastAPI    | http://SERVER_IP:8000 |
| Django     | http://SERVER_IP:8009 |
| Prometheus | http://SERVER_IP:9090 |
| Grafana    | http://SERVER_IP:3000 |

---

#  Grafana Setup

Login:

```
Username: admin
Password: admin
```

Add datasource:

```
Settings → Data Sources → Prometheus
```

URL:

```
http://prometheus:9090
```

---

# FastAPI Monitoring Queries

(Using Instrumentator metrics)

---

## Total Requests

```promql
sum(http_requests_total{job="fastapi"})
```

---

##  Requests Per Second

```promql
sum(rate(http_requests_total{job="fastapi"}[1m]))
```

---

##  Requests Per Endpoint

```promql
sum by (handler)(
  rate(http_requests_total{job="fastapi"}[1m])
)
```

---

##  Requests By HTTP Method

```promql
sum by (method)(
  rate(http_requests_total{job="fastapi"}[1m])
)
```

---

## Error Rate (5xx)

```promql
sum(
  rate(
    http_requests_total{
      job="fastapi",
      status=~"5.."
    }[1m]
  )
)
```

---

## API Latency (P95)

```promql
histogram_quantile(
  0.95,
  sum(rate(http_request_duration_seconds_bucket[1m])) by (le)
)
```

---

#  Django Monitoring Queries

---

##  Total Requests

```promql
sum(django_http_requests_total_by_method_total{job="django"})
```

---

## Requests/sec

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

---

##  Requests by Status Code

```promql
sum by (status)(
  rate(django_http_responses_total_by_status_total{job="django"}[1m])
)
```

---

##  Django Error Rate

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

---

#  Generate Test Traffic

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

Prometheus retention:

```
--storage.tsdb.retention.time=60d
```

Stores monitoring history for **60 days**.

---



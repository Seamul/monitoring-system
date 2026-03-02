

# Centralized Application Monitoring System

## FastAPI + Django + Prometheus + Grafana

This project provides a **centralized monitoring platform** for multiple backend services using:

* **Prometheus** → Metrics collection & storage
* **Grafana** → Visualization dashboards
* **Node Exporter** → Server resource monitoring
* **FastAPI** → Application metrics
* **Django** → Application metrics

---

**Node Exporter runs ON the server** and reads system information.

Main job:

* Collect server hardware & OS data

 Collects:

* CPU usage
* RAM usage
* Disk usage
* Network traffic
* System load

Output:
It exposes metrics at:

```
http://server-ip:9100/metrics
```

 Node Exporter **does NOT store data**
 Node Exporter **does NOT create dashboards**

It only says:

> “Here is my server information.”

---

## Prometheus — Data Collector & Database

**Prometheus collects data from exporters** like Node Exporter.

 Main job:

* Pull metrics from targets
* Store metrics
* Query metrics
* Trigger alerts

Prometheus regularly does:

```
Hey Node Exporter,
give me latest metrics
```

Then it:

* Saves data
* Keeps history
* Allows analysis

 Prometheus **stores monitoring data**.

---
---

##  How They Work Together

```
Server Resources
     ↓
Node Exporter
     ↓
Prometheus
     ↓
Grafana
```
---

#  Architecture Overview

```
                                                 ┌──────────────┐
                                                 │   FastAPI     │
                                                 │   /metrics    │
                                                 └──────┬───────┘
                                                        │
                                                        │
                ┌──────▼───────┐                        
                │    Django     │                       │
                │   /metrics    │
                └──────┬───────┘                        │
                       │                                ▼
                       -----------------------▼
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

# Monitored Metrics

## Application Metrics

 Total API Requests,
 Endpoint-wise Requests,
 HTTP Method Usage,
 Request Rate

## System Metrics

CPU Usage,
Memory Usage,
Disk Usage,
Network Usage

---

#  FastAPI Metrics Implementation

## `main.py`

```python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


# Auto Prometheus instrumentation
Instrumentator().instrument(app).expose(app)
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


Start monitoring:

```bash
docker compose up -d
```

---

# Service Access

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
http://172.16.5.7:9090
```

Click **Save & Test**

---

# Useful Prometheus Queries

## Total Requests
# Fast api Requests:

```
http_requests_total
```
## Show speacific port
```
http_requests_total{
 instance="172.16.5.7:8000",
}
```
---

## Fast api Requests total

```
sum(http_requests_total)
```

---



---

## Fast api Requests Per Second

```
rate(http_requests_total[1m])
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








import os
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://127.0.0.1:4317"
from fastapi.testclient import TestClient
from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_work():
    with TestClient(app) as client:
        response = client.get("/work?delay_ms=1")
        assert response.status_code == 200
        assert response.json()["result"] == "completed"


def test_metrics_exposes_custom_metric():
    with TestClient(app) as client:
        client.get("/work?delay_ms=1")
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "demo_http_requests_total" in response.text

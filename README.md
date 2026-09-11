# Kubernetes Observability Lab

Production-style Kubernetes observability portfolio project covering the three core telemetry signals: **metrics, logs and traces**.

## Architecture

```text
FastAPI demo service
   ├── Prometheus metrics ──> ServiceMonitor ──> Prometheus ──> Grafana
   ├── structured stdout logs ──> Grafana Alloy ──> Loki ──> Grafana
   └── OTLP traces ──> OpenTelemetry Collector ──> Tempo ──> Grafana

Kubernetes cluster telemetry
   ├── kube-state-metrics
   ├── node-exporter
   ├── kubelet / cAdvisor
   └── Alertmanager + PrometheusRule
```

## What this repository demonstrates

- Kubernetes observability design using metrics, logs and distributed tracing
- Prometheus Operator / `kube-prometheus-stack`
- Grafana dashboards and alerting
- Loki log aggregation with Grafana Alloy collection
- Tempo tracing backend
- OpenTelemetry Collector OTLP pipeline
- `ServiceMonitor` and `PrometheusRule` CRDs
- FastAPI application instrumentation
- health, readiness and metrics endpoints
- SLO-style alerting and troubleshooting runbooks
- GitHub Actions tests and manifest validation
- security, RBAC and cost considerations

## Repository structure

```text
app/                 instrumented FastAPI demo workload
k8s/                 application, ServiceMonitor and alert manifests
helm-values/         Prometheus/Grafana, Loki, Tempo, Alloy and OTel values
grafana/dashboards/  source-controlled custom dashboard JSON
scripts/             install, verify, load and uninstall helpers
docs/                architecture, runbook, interview guide and evidence plan
.github/workflows/    CI
```

## Quick start

Prerequisites: Docker, Kubernetes, kubectl and Helm 3.

```bash
make test
make install-observability
make deploy-app
make verify
```

Then port-forward Grafana:

```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3000:80
```

Open `http://localhost:3000` and inspect the **Kubernetes Observability Lab** dashboard.

## Key interview story

The application exposes Prometheus metrics and sends OTLP traces. Prometheus discovers the workload through a `ServiceMonitor`. Grafana Alloy collects Kubernetes pod logs and forwards them to Loki. The OpenTelemetry Collector receives traces and exports them to Tempo. Grafana provides a single exploration layer across all three signals, while Alertmanager routes Prometheus alerts. This lets an operator move from a latency alert, to the affected pod metrics, to its logs, and finally to a distributed trace.

## Current technology notes

The project intentionally uses `ServiceMonitor` and `PrometheusRule` from the Prometheus Operator ecosystem. For logs it uses Grafana Alloy rather than legacy Promtail. Loki is configured in monolithic mode for a small lab cluster; production-scale deployments should use appropriately sized object storage and scalable deployment patterns. Tempo is likewise configured as a lightweight lab backend, not as a production HA topology.

## Evidence

The repo includes local validation and an evidence checklist. Do not claim a live cluster deployment until you have added real screenshots from your own cluster under `docs/screenshots/`.

## License
MIT

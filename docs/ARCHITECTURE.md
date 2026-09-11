# Architecture

## Signals

### Metrics
The demo API exposes `/metrics`. A Prometheus Operator `ServiceMonitor` discovers the service and Prometheus stores time-series data. Grafana queries Prometheus. `PrometheusRule` objects define alert conditions routed through Alertmanager.

### Logs
The workload writes JSON logs to stdout. Grafana Alloy runs as a DaemonSet, discovers Kubernetes pod logs, adds Kubernetes labels, and forwards the streams to Loki.

### Traces
FastAPI is instrumented with OpenTelemetry. OTLP/gRPC spans are sent to an OpenTelemetry Collector deployment, enriched with Kubernetes attributes, batched, and exported to Tempo.

## Why separate telemetry backends?
Prometheus is optimized for numeric time-series metrics, Loki for indexed log metadata with compressed log chunks, and Tempo for trace spans. Grafana provides correlation across these stores without forcing one database to serve incompatible access patterns.

## Lab vs production
The repo deliberately uses single-replica Loki/Tempo-style lab deployments to keep resource requirements modest. Production would require HA, object storage, persistent volume strategy, authentication, TLS, backup, retention policies, resource sizing, tenancy, and controlled network access.

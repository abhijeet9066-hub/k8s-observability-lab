# Deployment Evidence Checklist

Add genuine screenshots only after deployment:

1. `01-monitoring-pods.png` — Prometheus/Grafana/Loki/Tempo/Alloy/OTel pods running
2. `02-demo-pods.png` — demo application replicas healthy
3. `03-prometheus-target.png` — application target UP
4. `04-grafana-dashboard.png` — request rate, p95 latency and error ratio
5. `05-loki-logs.png` — structured app logs with namespace/pod labels
6. `06-tempo-trace.png` — trace for a `/work` request
7. `07-alert-fired.png` — synthetic latency/error alert
8. `08-kubectl-resources.png` — ServiceMonitor and PrometheusRule resources

Do not use fabricated screenshots or claim cluster execution without real evidence.

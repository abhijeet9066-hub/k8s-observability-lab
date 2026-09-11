# Troubleshooting Runbook

## Alert: high error rate
1. Open the alert in Alertmanager/Grafana.
2. Check `demo_http_requests_total` by status and pod.
3. Inspect deployment replica health and restart counts.
4. Query Loki for the affected namespace/pod and `status=500` events.
5. Follow a trace from the same time range in Tempo.
6. Decide whether the issue is application, dependency, node or capacity related.

## Alert: high p95 latency
1. Confirm the latency increase in Prometheus.
2. Compare CPU throttling, memory and pod count.
3. Check HPA/replicas if configured.
4. Use logs for slow-path clues.
5. Use traces to identify the slow operation.

## No application metrics
- confirm `/metrics` responds
- confirm Service labels match `ServiceMonitor.spec.selector`
- confirm Prometheus is allowed to discover ServiceMonitors outside the monitoring namespace
- inspect Prometheus targets

## No logs
- inspect Alloy pod status and RBAC
- inspect Alloy logs
- verify Loki gateway service and push URL

## No traces
- verify application OTLP endpoint
- inspect OpenTelemetry Collector logs
- confirm Collector receiver port 4317
- confirm Tempo OTLP receiver and service DNS

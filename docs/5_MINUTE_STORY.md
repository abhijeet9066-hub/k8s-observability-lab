# Five-Minute Project Story

I wanted a Kubernetes project that demonstrated operations rather than only deployment manifests. I therefore built an observability lab around the three telemetry pillars: metrics, logs and traces.

The workload is a small FastAPI service with health and readiness endpoints. It exposes custom Prometheus counters and histograms for request rate, error rate, latency and a sample business event. I instrumented it with OpenTelemetry so each request can generate a trace.

For metrics, the Kubernetes Service is selected by a Prometheus Operator ServiceMonitor. Prometheus stores the time series and a PrometheusRule defines alerts for error ratio and p95 latency. Alertmanager is part of the monitoring stack.

For logs, the application emits structured JSON to stdout. Grafana Alloy runs on the nodes, discovers pod logs through Kubernetes metadata and forwards them to Loki. For traces, the application exports OTLP to an OpenTelemetry Collector. The collector enriches and batches spans before sending them to Tempo.

Grafana becomes the common investigation interface. An operator can begin with an alert, inspect the metric trend, open logs for the same pod and time window, and then inspect a trace to understand where latency occurred.

The repository also documents production gaps. The included Loki and Tempo configurations are intentionally small-lab topologies. A production version would use HA, object storage, authentication, TLS, restricted RBAC, network policies, external secrets, retention controls, and tuned sampling/cardinality.

What I learned most from the project is that observability is not just installing dashboards. It is designing telemetry so that an operational question can be followed across signals with enough context to reach a root cause.

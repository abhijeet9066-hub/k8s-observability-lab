# Interview Guide

## 60-second explanation
I built a Kubernetes observability lab that unifies metrics, logs and traces. A FastAPI service exposes custom Prometheus metrics and emits OpenTelemetry traces. Prometheus discovers metrics through a ServiceMonitor, Grafana Alloy collects container logs into Loki, and the OpenTelemetry Collector exports traces into Tempo. Grafana correlates all three signals, while PrometheusRule and Alertmanager provide SLO-style alerting.

## Questions you should be ready for

### Monitoring vs observability
Monitoring tells me when known conditions cross thresholds. Observability is the broader ability to understand internal system behavior from telemetry, especially when the failure mode was not pre-defined.

### Why Prometheus?
It is a Kubernetes-native fit for time-series metrics and label-based dimensional queries. The Operator ecosystem gives declarative ServiceMonitor and PrometheusRule resources.

### Why not put logs in Prometheus?
Prometheus is not designed as a log store. Logs have different cardinality, retention and query patterns.

### Why OpenTelemetry?
It standardizes instrumentation and transport so application code is less coupled to a specific tracing backend.

### Why a Collector?
It centralizes enrichment, batching, sampling/routing and backend credentials rather than pushing that complexity into every application.

### What is a ServiceMonitor?
A Prometheus Operator CRD describing how Prometheus should discover and scrape a Kubernetes Service.

### What is an SLO-style alert?
An alert tied to user-relevant service behavior such as error ratio or latency instead of only infrastructure symptoms.

### What would you change for production?
HA replicas, object storage, authentication/TLS, retention and compaction policies, external secrets, restrictive NetworkPolicies, resource tuning, remote storage/managed services, backup, and alert routing with ownership/escalation.

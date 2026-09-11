# Security and Cost Notes

## Security
- the demo workload runs as non-root and drops Linux capabilities
- use NetworkPolicies to restrict telemetry egress and UI access
- store Grafana/admin/backend credentials outside Git in Secrets or an external secret manager
- place authentication/TLS in front of Grafana, Loki and Tempo for real deployments
- minimize collector and Alloy RBAC to only enabled discovery features
- avoid exposing telemetry endpoints publicly

## Cost
Major cost drivers are metrics cardinality, scrape interval, log volume/retention and trace sampling/retention. Production designs should define retention classes, recording rules, sampling, log filtering and object-storage lifecycle policies.

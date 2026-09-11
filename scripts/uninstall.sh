#!/usr/bin/env bash
set -euo pipefail
kubectl delete namespace observability-demo --ignore-not-found
for release in alloy otel-collector tempo loki kube-prometheus-stack; do
  helm uninstall "$release" -n monitoring 2>/dev/null || true
done
kubectl delete namespace monitoring --ignore-not-found

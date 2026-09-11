#!/usr/bin/env bash
set -euo pipefail
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts --force-update
helm repo add grafana https://grafana.github.io/helm-charts --force-update
helm repo add grafana-community https://grafana-community.github.io/helm-charts --force-update
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts --force-update
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring -f helm-values/kube-prometheus-stack-values.yaml
helm upgrade --install loki grafana-community/loki \
  -n monitoring -f helm-values/loki-values.yaml
helm upgrade --install tempo grafana-community/tempo \
  -n monitoring -f helm-values/tempo-values.yaml
helm upgrade --install otel-collector open-telemetry/opentelemetry-collector \
  -n monitoring -f helm-values/otel-collector-values.yaml
helm upgrade --install alloy grafana/alloy \
  -n monitoring -f helm-values/alloy-values.yaml

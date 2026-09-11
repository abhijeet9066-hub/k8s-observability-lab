#!/usr/bin/env bash
set -euo pipefail
kubectl get pods -n monitoring
kubectl get pods -n observability-demo
kubectl get servicemonitors -A
kubectl get prometheusrules -A
kubectl get svc -n monitoring

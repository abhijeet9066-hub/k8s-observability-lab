.PHONY: test install-observability deploy-app verify load uninstall

test:
	python -m pytest -q app/tests

install-observability:
	bash scripts/install_observability.sh

deploy-app:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/app.yaml
	kubectl apply -f k8s/servicemonitor.yaml
	kubectl apply -f k8s/prometheusrule.yaml

verify:
	bash scripts/verify.sh

load:
	python scripts/generate_load.py

uninstall:
	bash scripts/uninstall.sh

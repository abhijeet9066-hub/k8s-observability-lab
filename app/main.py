import json
import logging
import os
import random
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "observability-demo-api")
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector.monitoring.svc.cluster.local:4317")

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(SERVICE_NAME)

REQUESTS = Counter("demo_http_requests_total", "HTTP requests", ["path", "status"])
LATENCY = Histogram(
    "demo_http_request_duration_seconds",
    "Request duration",
    ["path"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)
BUSINESS_EVENTS = Counter("demo_business_events_total", "Synthetic checkout outcomes", ["outcome"])


def configure_tracing() -> None:
    if not OTEL_AVAILABLE:
        logger.warning("opentelemetry_instrumentation_not_installed")
        return
    provider = TracerProvider(resource=Resource.create({"service.name": SERVICE_NAME}))
    try:
        exporter = OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))
    except Exception:
        logger.exception("trace_exporter_configuration_failed")
    trace.set_tracer_provider(provider)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_tracing()
    logger.info(json.dumps({"event": "service_started", "service": SERVICE_NAME}))
    yield


app = FastAPI(title="Kubernetes Observability Demo", version="1.0.0", lifespan=lifespan)
if OTEL_AVAILABLE:
    FastAPIInstrumentor.instrument_app(app)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    return {"ready": True}


@app.get("/work")
def work(delay_ms: int = 40, fail: bool = False):
    started = time.perf_counter()
    path = "/work"
    delay_ms = max(0, min(delay_ms, 3000))
    time.sleep(delay_ms / 1000)
    status = "500" if fail else "200"
    REQUESTS.labels(path=path, status=status).inc()
    LATENCY.labels(path=path).observe(time.perf_counter() - started)
    logger.info(json.dumps({"event": "work_request", "delay_ms": delay_ms, "status": status}))
    if fail:
        raise HTTPException(status_code=500, detail="synthetic failure")
    return {"result": "completed", "delay_ms": delay_ms}


@app.post("/checkout")
def checkout():
    outcome = random.choices(["approved", "declined"], weights=[0.93, 0.07], k=1)[0]
    BUSINESS_EVENTS.labels(outcome=outcome).inc()
    logger.info(json.dumps({"event": "checkout", "outcome": outcome}))
    return {"outcome": outcome}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

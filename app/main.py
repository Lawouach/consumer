import time
from typing import Dict

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

latency = 0.0


def get_latency() -> float:
    return latency


def set_latency(value: float) -> None:
    global latency
    latency = value


@app.get("/")
def index() -> Dict[str, str]:
    if latency > 0:
        time.sleep(latency)
    return {"Hello": "The World"}


@app.get("/health")
def health() -> str:
    return ""


@app.get("/inject/latency")
def inject_latency(value: float = 0) -> str:
    set_latency(value)
    return ""

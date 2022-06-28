import asyncio
import os
import time
from typing import Any, Dict

from fastapi import FastAPI
import httpx
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import JSONResponse


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

latency = 0.0


def get_latency() -> float:
    return latency


def set_latency(value: float) -> None:
    global latency
    latency = value


@app.get("/consumer")
def index() -> Dict[str, str]:
    if latency > 0:
        time.sleep(latency)
    return {"Hello": "The World"}


@app.get("/consumer/data")
async def data() -> JSONResponse:
    if latency > 0:
        await asyncio.sleep(latency)

    async with httpx.AsyncClient() as client:
        r = await client.get(os.getenv("PRODUCER_URL"))  # type: ignore
        if r.status_code != 200:
            return JSONResponse(status_code=500, content="")

        return JSONResponse(
            {
                "data": r.json(),
                "status": r.status_code,
                "duration": r.elapsed.total_seconds(),
            }
        )


@app.get("/health")
def health() -> str:
    return ""


@app.get("/consumer/inject/latency")
def inject_latency(value: float = 0) -> str:
    set_latency(value)
    return ""

import os
import time
from unittest.mock import ANY

from fastapi.testclient import TestClient
from httpx import Response
import pytest
import respx

from .main import app, get_latency, set_latency

client = TestClient(app)


def test_index() -> None:
    response = client.get("/consumer")
    assert response.status_code == 200
    assert response.json() == {"Hello": "The World"}


def test_index_with_latency() -> None:
    set_latency(0.51)
    s = time.time()
    response = client.get("/consumer")
    e = time.time()

    assert e - s > 0.5
    assert response.status_code == 200
    assert response.json() == {"Hello": "The World"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == ""


def test_set_latency() -> None:
    response = client.get("/consumer/inject/latency?value=0.45")
    assert response.status_code == 200
    assert response.json() == ""
    assert get_latency() == 0.45


@pytest.mark.asyncio
@respx.mock
async def test_data() -> None:
    url = "http://example.com"
    os.environ["PRODUCER_URL"] = url

    d = {"message": "hello there"}
    r = respx.get(url).mock(return_value=Response(200, json=d))

    response = client.get("/consumer/data")
    assert response.status_code == 200
    assert response.json() == {"data": d, "status": 200, "duration": ANY}


@pytest.mark.asyncio
@respx.mock
async def test_data_on_producer_error() -> None:
    url = "http://example.com"
    os.environ["PRODUCER_URL"] = url

    d = {"message": "hello there"}
    r = respx.get(url).mock(return_value=Response(400))

    response = client.get("/consumer/data")
    assert response.status_code == 500


@pytest.mark.asyncio
@respx.mock
async def test_data_with_latency() -> None:
    response = client.get("/consumer/inject/latency?value=0.45")

    url = "http://example.com"
    os.environ["PRODUCER_URL"] = url

    d = {"message": "hello there"}
    r = respx.get(url).mock(return_value=Response(200, json=d))

    response = client.get("/consumer/data")
    assert response.status_code == 200
    assert response.json() == {"data": d, "status": 200, "duration": ANY}

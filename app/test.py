import time

from fastapi.testclient import TestClient

from .main import app, get_latency, set_latency

client = TestClient(app)


def test_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "The World"}


def test_index_with_latency() -> None:
    set_latency(0.51)
    s = time.time()
    response = client.get("/")
    e = time.time()

    assert e - s > 0.5
    assert response.status_code == 200
    assert response.json() == {"Hello": "The World"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == ""


def test_set_latency() -> None:
    response = client.get("/inject/latency?value=0.45")
    assert response.status_code == 200
    assert response.json() == ""
    assert get_latency() == 0.45

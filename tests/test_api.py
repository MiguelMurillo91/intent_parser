from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from intent_parser.api import app, get_llm_client
from intent_parser.llm import FakeLLM

VALID_JSON = (
    '{"intent_type": "device_control", "device": "switch 1", '
    '"room": "Main Room", "action": "off", "confidence": 0.94}'
)


@pytest.fixture
def client_with_fake() -> Iterator[TestClient]:
    """A TestClient whose LLM is a fake returning VALID_JSON."""
    app.dependency_overrides[get_llm_client] = lambda: FakeLLM(VALID_JSON)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health():
    assert TestClient(app).get("/health").json() == {"status": "ok"}


def test_parse_returns_intent(client_with_fake: TestClient):
    response = client_with_fake.post("/parse", json={"text": "turn off switch 1"})
    assert response.status_code == 200
    body = response.json()
    assert body["device"] == "switch 1"
    assert body["room"] == "main_room"
    assert body["action"] == "off"


def test_parse_rejects_missing_text():
    assert TestClient(app).post("/parse", json={"wrong_key": "oops"}).status_code == 422

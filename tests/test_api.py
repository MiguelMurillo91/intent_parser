from fastapi.testclient import TestClient

from intent_parser.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_parse_rejects_missing_text():
    response = client.post("/parse", json={"wrong_key": "oops"})
    assert response.status_code == 422

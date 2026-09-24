from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "triahome-api",
    }


def test_diagnose_returns_valid_response():
    response = client.post("/diagnose")

    assert response.status_code == 200

    data = response.json()

    assert data["problem"]["category"] == "plumbing"
    assert 0 <= data["problem"]["confidence"] <= 1

    assert data["safety"]["risk_level"] in {
        "low",
        "medium",
        "high",
        "emergency",
    }

    assert isinstance(data["diagnosis"]["likely_causes"], list)
    assert isinstance(data["parts"], list)
    assert isinstance(data["steps"], list)
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
    response = client.post(
        "/diagnose",
        json={
            "description": (
                "The pipe under my kitchen sink leaks "
                "when the washing machine drains."
            )
        },
    )

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


def test_diagnose_accepts_relevant_property_problem():
    response = client.post(
        "/diagnose",
        json={
            "description": (
                "The pipe under my kitchen sink leaks "
                "when the washing machine drains."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "problem" in data
    assert "safety" in data
    assert "diagnosis" in data
    assert "resolution" in data


def test_diagnose_rejects_missing_description():
    response = client.post(
        "/diagnose",
        json={},
    )

    assert response.status_code == 422


def test_diagnose_rejects_empty_description():
    response = client.post(
        "/diagnose",
        json={
            "description": "",
        },
    )

    assert response.status_code == 422


def test_diagnose_rejects_out_of_scope_description():
    response = client.post(
        "/diagnose",
        json={
            "description": "Can you write a CV for me?"
        },
    )

    assert response.status_code == 400
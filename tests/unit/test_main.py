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

def test_create_repair_case():
    response = client.post(
        "/cases",
        json={
            "description": "The pipe under my kitchen sink is leaking."
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["description"] == (
        "The pipe under my kitchen sink is leaking."
    )
    assert data["status"] == "new"
    assert data["evidence"] == []
    assert "id" in data
    assert data["id"]


def test_create_repair_case_rejects_missing_description():
    response = client.post(
        "/cases",
        json={},
    )

    assert response.status_code == 422


def test_create_repair_case_rejects_missing_description():
    response = client.post(
        "/cases",
        json={},
    )

    assert response.status_code == 422


def test_create_repair_case_rejects_out_of_scope_description():
    response = client.post(
        "/cases",
        json={
            "description": "Can you write a CV for me?"
        },
    )

    assert response.status_code == 400


def test_repair_case_response_has_evidence_list():
    response = client.post(
        "/cases",
        json={
            "description": "The pipe under my kitchen sink is leaking."
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "evidence" in data
    assert isinstance(data["evidence"], list)
    assert data["evidence"] == []


def test_get_repair_case():
    create_response = client.post(
        "/cases",
        json={
            "description": "The pipe under my kitchen sink is leaking."
        },
    )

    assert create_response.status_code == 201

    created_case = create_response.json()
    case_id = created_case["id"]

    get_response = client.get(f"/cases/{case_id}")

    assert get_response.status_code == 200
    assert get_response.json() == created_case


def test_add_text_evidence_to_repair_case():
    create_response = client.post(
        "/cases",
        json={
            "description": "The pipe under my kitchen sink is leaking."
        },
    )

    assert create_response.status_code == 201

    case_id = create_response.json()["id"]

    evidence_response = client.post(
        f"/cases/{case_id}/evidence",
        json={
            "type": "text",
            "content": "The leak only happens when the washing machine drains."
        },
    )

    assert evidence_response.status_code == 201

    evidence = evidence_response.json()

    assert evidence["type"] == "text"
    assert evidence["content"] == (
        "The leak only happens when the washing machine drains."
    )
    assert "id" in evidence
    assert evidence["id"]


def test_text_evidence_is_saved_to_repair_case():
    # Create a Repair Case
    create_response = client.post(
        "/cases",
        json={
            "description": "The pipe under my kitchen sink is leaking."
        },
    )

    assert create_response.status_code == 201
    case_id = create_response.json()["id"]

    # Add text evidence
    evidence_response = client.post(
        f"/cases/{case_id}/evidence",
        json={
            "type": "text",
            "content": "The leak only happens when the washing machine drains."
        },
    )

    assert evidence_response.status_code == 201

    # Retrieve the Repair Case again
    get_response = client.get(f"/cases/{case_id}")

    assert get_response.status_code == 200

    repair_case = get_response.json()

    # Confirm the evidence was stored
    assert len(repair_case["evidence"]) == 1

    evidence = repair_case["evidence"][0]

    assert evidence["type"] == "text"
    assert evidence["content"] == (
        "The leak only happens when the washing machine drains."
    )
    assert evidence["id"]
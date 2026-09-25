from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app.ai import is_property_issue, diagnose_property_issue

from app.cases import (
    add_evidence,
    get_repair_case,
    save_repair_case,
)

from app.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    RepairCase,
    RepairCaseCreate,
    Evidence,
    EvidenceCreate,
)

app = FastAPI(
    title="Triahome API",
    description="AI-powered home repair triage",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "triahome-api",
    }


@app.post("/diagnose", response_model=DiagnosisResponse)
def diagnose(request: DiagnosisRequest):
    if not is_property_issue(request.description):
        raise HTTPException(
            status_code=400,
            detail="Description is outside Tria Home's property repair scope.",
        )

    return diagnose_property_issue(request.description)


@app.post("/cases", response_model=RepairCase, status_code=201)
def create_repair_case(request: RepairCaseCreate):
    if not is_property_issue(request.description):
        raise HTTPException(
            status_code=400,
            detail="Description is outside Tria Home's property repair scope.",
        )

    repair_case = RepairCase(
        id=str(uuid4()),
        description=request.description,
        status="new",
        evidence=[],
    )

    return save_repair_case( repair_case)


@app.get("/cases/{case_id}", response_model=RepairCase)
def read_repair_case(case_id: str):
    repair_case = get_repair_case(case_id)

    if repair_case is None:
        raise HTTPException(
            status_code=404,
            detail="Repair Case not found.",
        )

    return repair_case


@app.post(
    "/cases/{case_id}/evidence",
    response_model=Evidence,
    status_code=201,
)
def create_evidence(case_id: str, request: EvidenceCreate):
    evidence = Evidence(
        id=str(uuid4()),
        type=request.type,
        content=request.content,
    )

    repair_case = add_evidence(case_id, evidence)

    if repair_case is None:
        raise HTTPException(
            status_code=404,
            detail="Repair Case not found.",
        )

    return evidence


def test_invalid_evidence_does_not_modify_repair_case():
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
            "content": ""
        },
    )

    assert evidence_response.status_code == 422

    get_response = client.get(f"/cases/{case_id}")

    assert get_response.status_code == 200

    repair_case = get_response.json()

    assert repair_case["evidence"] == []
from fastapi import FastAPI, HTTPException
from uuid import uuid4

from app.ai import is_property_issue, diagnose_property_issue
from app.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    RepairCase,
    RepairCaseCreate,
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
    return RepairCase(
        id=str(uuid4()),
        description=request.description,
        status="new",
        evidence=[],
    )
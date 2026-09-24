from typing import Literal

from pydantic import BaseModel, Field


class Problem(BaseModel):
    category: str
    summary: str
    confidence: float = Field(ge=0, le=1)


class Safety(BaseModel):
    risk_level: Literal["low", "medium", "high", "emergency"]
    hazards: list[str] = []
    immediate_action: str | None = None


class LikelyCause(BaseModel):
    cause: str
    confidence: float = Field(ge=0, le=1)


class Diagnosis(BaseModel):
    likely_causes: list[LikelyCause] = []
    additional_evidence_needed: list[str] = []


class Resolution(BaseModel):
    safe_to_diy: bool
    professional_required: bool
    recommended_action: str


class Part(BaseModel):
    name: str
    quantity: int = 1
    specification: str | None = None
    search_terms: list[str] = []


class RepairStep(BaseModel):
    step: int
    instruction: str
    safety_note: str | None = None


class DiagnosisResponse(BaseModel):
    problem: Problem
    safety: Safety
    diagnosis: Diagnosis
    resolution: Resolution
    parts: list[Part] = []
    steps: list[RepairStep] = []
from fastapi import FastAPI, HTTPException

from app.ai import is_property_issue
from app.schemas import DiagnosisRequest, DiagnosisResponse

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

        return {
        "problem": {
            "category": "plumbing",
            "summary": "Leak from the waste pipe connection under the sink",
            "confidence": 0.2,
        },
        "safety": {
            "risk_level": "low",
            "hazards": [
                "Water may damage the cabinet or surrounding materials"
            ],
            "immediate_action": "Stop using the sink until the connection is checked",
        },
        "diagnosis": {
            "likely_causes": [
                {
                    "cause": "Missing or incorrectly fitted conical washer",
                    "confidence": 0.88,
                },
                {
                    "cause": "Loose waste pipe connection",
                    "confidence": 0.72,
                },
            ],
            "additional_evidence_needed": [
                "Close-up photo of the pipe joint after the nut is removed"
            ],
        },
        "resolution": {
            "safe_to_diy": True,
            "professional_required": False,
            "recommended_action": (
                "Inspect the waste connection and fit the correct washer "
                "before tightening the joint."
            ),
        },
        "parts": [
            {
                "name": "Conical waste pipe washer",
                "quantity": 1,
                "specification": "Size must match the existing waste pipe",
                "search_terms": [
                    "sink waste pipe conical washer",
                    "waste pipe compression washer",
                ],
            }
        ],
        "steps": [
            {
                "step": 1,
                "instruction": "Place a container or towel underneath the joint.",
                "safety_note": None,
            },
            {
                "step": 2,
                "instruction": "Unscrew the waste pipe connection and inspect the joint.",
                "safety_note": "Do not use the sink while the connection is open.",
            },
            {
                "step": 3,
                "instruction": "Fit the correct washer and reconnect the pipe.",
                "safety_note": None,
            },
            {
                "step": 4,
                "instruction": "Run a small amount of water and check for leaks.",
                "safety_note": None,
            },
        ],
    }
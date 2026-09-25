def is_property_issue(description: str) -> bool:
    """
    Temporary scope gate.

    This will later be replaced by AI-based classification.
    """
    property_terms = {
        "sink",
        "pipe",
        "leak",
        "toilet",
        "tap",
        "drain",
        "boiler",
        "radiator",
        "door",
        "window",
        "wall",
        "ceiling",
        "floor",
        "washing machine",
        "dishwasher",
    }

    description_lower = description.lower()

    return any(
        term in description_lower
        for term in property_terms
    )



def diagnose_property_issue(description: str) -> dict:
    """
    Return a deterministic mock diagnosis for a property issue.

    This will later be replaced by the real diagnostic engine.
    """
    return {
        "problem": {
            "category": "plumbing",
            "summary": description,
            "confidence": 0.92,
        },
        "safety": {
            "risk_level": "low",
            "hazards": [
                "Water may damage the cabinet or surrounding materials"
            ],
            "immediate_action": (
                "Stop using the sink until the connection is checked"
            ),
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
                "instruction": (
                    "Place a container or towel underneath the joint."
                ),
                "safety_note": None,
            },
            {
                "step": 2,
                "instruction": (
                    "Unscrew the waste pipe connection and inspect the joint."
                ),
                "safety_note": (
                    "Do not use the sink while the connection is open."
                ),
            },
            {
                "step": 3,
                "instruction": (
                    "Fit the correct washer and reconnect the pipe."
                ),
                "safety_note": None,
            },
            {
                "step": 4,
                "instruction": (
                    "Run a small amount of water and check for leaks."
                ),
                "safety_note": None,
            },
        ],
    }
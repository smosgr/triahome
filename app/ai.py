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
from app.schemas import RepairCase, Evidence


repair_cases: dict[str, RepairCase] = {}


def save_repair_case(repair_case: RepairCase) -> RepairCase:
    repair_cases[repair_case.id] = repair_case
    return repair_case


def get_repair_case(case_id: str) -> RepairCase | None:
    return repair_cases.get(case_id)


def add_evidence(
    case_id: str,
    evidence: Evidence,
) -> RepairCase | None:
    repair_case = repair_cases.get(case_id)

    if repair_case is None:
        return None

    repair_case.evidence.append(evidence)

    return repair_case
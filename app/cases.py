from datetime import timezone
from sqlalchemy import select

from app.database import SessionLocal
from app.models import EvidenceModel, RepairCaseModel
from app.schemas import Evidence, RepairCase


def save_repair_case(repair_case: RepairCase) -> RepairCase:
    db_case = RepairCaseModel(
        id=repair_case.id,
        description=repair_case.description,
        status=repair_case.status,
        created_at=repair_case.created_at,
    )

    with SessionLocal() as db:
        db.add(db_case)
        db.commit()

    return repair_case


def get_repair_case(case_id: str) -> RepairCase | None:
    with SessionLocal() as db:
        db_case = db.scalar(
            select(RepairCaseModel).where(
                RepairCaseModel.id == case_id
            )
        )

        if db_case is None:
            return None

        created_at = db_case.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        evidence = [
            Evidence(
                id=db_evidence.id,
                type=db_evidence.type,
                content=db_evidence.content,
            )
            for db_evidence in db_case.evidence
        ]

        return RepairCase(
            id=db_case.id,
            description=db_case.description,
            status=db_case.status,
            created_at=created_at,
            evidence=evidence,
        )


def add_evidence(
    case_id: str,
    evidence: Evidence,
) -> RepairCase | None:
    with SessionLocal() as db:
        db_case = db.get(RepairCaseModel, case_id)

        if db_case is None:
            return None

        db_evidence = EvidenceModel(
            id=evidence.id,
            case_id=case_id,
            type=evidence.type,
            content=evidence.content,
        )

        db.add(db_evidence)
        db.commit()

    return get_repair_case(case_id)
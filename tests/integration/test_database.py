from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models import Base, EvidenceModel, RepairCaseModel


def test_repair_case_can_be_persisted(tmp_path):
    database_path = tmp_path / "test_tria.db"

    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    case_id = str(uuid4())

    repair_case = RepairCaseModel(
        id=case_id,
        description="The pipe under my kitchen sink is leaking.",
        status="new",
    )

    with TestSessionLocal() as db:
        db.add(repair_case)
        db.commit()

    with TestSessionLocal() as db:
        persisted_case = db.scalar(
            select(RepairCaseModel).where(
                RepairCaseModel.id == case_id
            )
        )

        assert persisted_case is not None
        assert persisted_case.id == case_id
        assert persisted_case.description == (
            "The pipe under my kitchen sink is leaking."
        )
        assert persisted_case.status == "new"
        assert persisted_case.created_at is not None


def test_evidence_can_be_persisted_for_repair_case(tmp_path):
    database_path = tmp_path / "test_tria.db"

    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    case_id = str(uuid4())
    evidence_id = str(uuid4())

    with TestSessionLocal() as db:
        repair_case = RepairCaseModel(
            id=case_id,
            description="The pipe under my kitchen sink is leaking.",
            status="new",
        )

        db.add(repair_case)
        db.commit()

        evidence = EvidenceModel(
            id=evidence_id,
            case_id=case_id,
            type="text",
            content="The leak happens when the washing machine drains.",
        )

        db.add(evidence)
        db.commit()

    with TestSessionLocal() as db:
        persisted_case = db.get(RepairCaseModel, case_id)

        assert persisted_case is not None
        assert len(persisted_case.evidence) == 1
        assert persisted_case.evidence[0].id == evidence_id
        assert persisted_case.evidence[0].type == "text"
        assert persisted_case.evidence[0].content == (
            "The leak happens when the washing machine drains."
        )
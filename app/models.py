from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RepairCaseModel(Base):
    __tablename__ = "repair_cases"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="new",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    evidence: Mapped[list["EvidenceModel"]] = relationship(
        back_populates="repair_case",
        cascade="all, delete-orphan",
    )


class EvidenceModel(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    case_id: Mapped[str] = mapped_column(
        ForeignKey("repair_cases.id"),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    repair_case: Mapped["RepairCaseModel"] = relationship(
        back_populates="evidence",
    )
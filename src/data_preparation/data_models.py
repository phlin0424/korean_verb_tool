import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, declared_attr, relationship

Base = declarative_base()


class KoreanVerbTable(Base):
    """Major tables to store the korean verbs."""

    __tablename__ = "korean_verbs"

    id = Column(
        Integer,
        primary_key=True,
        comment="Primary key for the table",
    )

    korean_verb = Column(
        String,
        nullable=False,
        comment="Korean verb, e.g., '쯕다'",
    )

    korean_verb_uuid = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Unique UUID for Korean verb",
    )
    variances = relationship("KoreanVerbVarianceBaseTable", back_populates="verb")


class KoreanVerbVarianceBaseTable(Base):
    """A abstract table for all verb variance tables."""

    __abstract__ = True

    @declared_attr
    def id(self) -> Mapped[int]:
        """Unique ID."""
        return mapped_column(
            Integer,
            primary_key=True,
            autoincrement=True,
            comment="Unique ID",
        )

    @declared_attr
    def korean_verb_uuid(self) -> Mapped[UUID]:
        """Foreign key referencing korean_verb_uuid in KoreanVerbTable."""
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("korean_verbs.korean_verb_uuid"),
            nullable=False,
            comment="Foreign key referencing korean_verb_uuid in KoreanVerbTable",
        )

    @declared_attr
    def audio(self) -> Mapped[String]:
        """Path to the Korean verb variance audio."""
        return mapped_column(
            String,
            nullable=True,
            comment="Path to the Korean verb variance audio.",
        )

    @declared_attr
    def verb(self) -> Mapped["KoreanVerbTable"]:
        """Relationship to link back to the KoreanVerbTable."""
        return relationship("KoreanVerbTable", back_populates="variances")


class KoreanVerbVarianceNegativeTable(KoreanVerbVarianceBaseTable):
    """A table to store korean verb variance (negative)."""

    __tablename__ = "korean_verbs_variances_negative"

    korean_verb_variance_negative = Column(
        String,
        nullable=False,
        comment="Negative form of the Korean verb. e.g., '안 쯕슨니다'",
    )

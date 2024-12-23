import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class KoreanVerbTable(Base):
    """Major tables to store the korean verbs."""

    __tablename__ = "korean_verb"

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

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Unique ID",
    )

    korean_verb_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("korean_verbs.korean_verb_uuid"),
        nullable=False,
        comment="Foreign key referencing korean_verb_uuid in KoreanVerbTable",
    )

    audio = Column(
        String,
        nullable=True,
        comment="Path to the Korean verb variance audio.",
    )

    # Relationship to link back to the KoreanVerbTable
    verb = relationship("KoreanVerbTable", back_populates="variances")


class KoreanVerbVarianceNegativeTable(KoreanVerbVarianceBaseTable):
    """A table to store korean verb variance (negative)."""

    __tablename__ = "korean_verb_variances_negative"

    korean_verb_variance_negative = Column(
        String,
        nullable=False,
        comment="Negative form of the Korean verb. e.g., '안 쯕슨니다'",
    )

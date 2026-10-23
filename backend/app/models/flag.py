from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Flag(Base):
    __tablename__ = "flags"
    __table_args__ = (
        UniqueConstraint("environment_id", "key", name="uq_flags_environment_key"),
        Index("ix_flags_key_environment", "key", "environment_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    environment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("environments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(150), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="boolean", server_default="boolean")
    default_value: Mapped[dict | list | bool | str | int | float | None] = mapped_column(JSONB)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    description: Mapped[str | None] = mapped_column(Text)
    owner_team: Mapped[str | None] = mapped_column(String(100))
    created_by: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    environment = relationship("Environment", back_populates="flags")
    creator = relationship("User", back_populates="flags_created")
    versions = relationship("FlagVersion", back_populates="flag", cascade="all, delete-orphan")
    targeting_rules = relationship("TargetingRule", back_populates="flag", cascade="all, delete-orphan")
    evaluation_stats = relationship("EvaluationStat", back_populates="flag", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="flag")

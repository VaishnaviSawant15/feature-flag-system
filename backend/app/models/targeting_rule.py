from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TargetingRule(Base):
    __tablename__ = "targeting_rules"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    flag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("flags.id", ondelete="CASCADE"), nullable=False, index=True
    )
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. user, group
    operator: Mapped[str | None] = mapped_column(String(50))            # e.g. in, equals
    attribute: Mapped[str | None] = mapped_column(String(100))          # e.g. user_id, group
    value: Mapped[dict | list | str | int | bool | None] = mapped_column(JSONB)
    result: Mapped[dict | list | str | int | bool | None] = mapped_column(JSONB)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    flag = relationship("Flag", back_populates="targeting_rules")

import datetime as dt

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class EvaluationStat(Base):
    __tablename__ = "evaluation_stats"
    __table_args__ = (
        UniqueConstraint("flag_id", "environment_id", "date", "hour", name="uq_eval_stats_bucket"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    flag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("flags.id", ondelete="CASCADE"), nullable=False, index=True
    )
    environment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("environments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    hour: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0, server_default="0")

    flag = relationship("Flag", back_populates="evaluation_stats")
    environment = relationship("Environment", back_populates="evaluation_stats")

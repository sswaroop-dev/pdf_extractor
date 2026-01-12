from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, Index, PrimaryKeyConstraint, UniqueConstraint, String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class OperationName(Base):
    __tablename__ = 'myapp_operation'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='myapp_operation_pkey'),
        UniqueConstraint('name', name='myapp_operation_name_uniq_key'),
        Index('idx_operation_name_like', 'name'),
        Index('idx_operation_code', 'code'),
    )
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), 
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True), 
        nullable=True,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    speed_and_feed: Mapped[list['SpeedAndFeed']] = relationship(
        'SpeedAndFeed', 
        back_populates='operation'
    )
    default_policy_v2: Mapped[list['DefaultPolicyV2']] = relationship(
        'DefaultPolicyV2',
        foreign_keys='DefaultPolicyV2.operation_id',
        back_populates='operation'
    )
    user_policy: Mapped[list['UserPolicy']] = relationship(
        'UserPolicy',
        foreign_keys='UserPolicy.operation_id',
        back_populates='operation'
    )

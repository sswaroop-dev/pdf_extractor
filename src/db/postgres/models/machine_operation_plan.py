from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, Double, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class MachineOperationPlan(Base):
    __tablename__ = 'myapp_machiningoperationplan'
    __table_args__ = (
        ForeignKeyConstraint(['cad_feature_cache_id'], ['myapp_cadfeaturecache.id'], deferrable=True, initially='DEFERRED', name='myapp_operations_cad_feature_cache_id_ed56a440_fk_myapp_cad'),
        PrimaryKeyConstraint('id', name='myapp_operations_pkey'),
        Index('idx_mop_job', 'cad_feature_cache_id') 

    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    operations: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    cad_feature_cache_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    setup_name: Mapped[Optional[str]] = mapped_column(String(100))
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

    job: Mapped[Optional['Job']] = relationship(
        'Job', 
        back_populates='machine_operation_plan'
    )

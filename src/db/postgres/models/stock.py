from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import (
    BigInteger, DateTime, Double, ForeignKeyConstraint, Index, 
    PrimaryKeyConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Stock(Base):
    __tablename__ = 'myapp_stock'
    __table_args__ = (
        ForeignKeyConstraint(['machine_id'], ['myapp_machine.id'], deferrable=True, initially='DEFERRED', name='myapp_stock_machine_id_ffc69d45_fk_myapp_machine_id'),
        PrimaryKeyConstraint('id', name='myapp_stock_pkey'),
        Index('idx_stock_machine', 'machine_id')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    machine_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    x: Mapped[Optional[float]] = mapped_column(Double(53))
    y: Mapped[Optional[float]] = mapped_column(Double(53))
    z: Mapped[Optional[float]] = mapped_column(Double(53))
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
    
    machine: Mapped['Machine'] = relationship(
        'Machine', 
        back_populates='stock'
    )
    job: Mapped[List['Job']] = relationship(
        'Job', 
        back_populates='stock'
    )
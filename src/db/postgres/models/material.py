from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import (
    BigInteger, DateTime, Index, PrimaryKeyConstraint, String, 
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Material(Base):
    __tablename__ = 'myapp_material'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='myapp_material_pkey'),
        UniqueConstraint('name', name='myapp_material_name_key'),
        Index('idx_material_name_like', 'name')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    en_number_1: Mapped[Optional[str]] = mapped_column(String(50))
    en_number_2: Mapped[Optional[str]] = mapped_column(String(50))
    composition_or_iso: Mapped[Optional[str]] = mapped_column(String(100))
    yield_strength: Mapped[Optional[str]] = mapped_column(String(100))
    tensile_strength: Mapped[Optional[str]] = mapped_column(String(100))
    elongation: Mapped[Optional[str]] = mapped_column(String(100))
    hardness: Mapped[Optional[str]] = mapped_column(String(100))
    modulus_elasticity: Mapped[Optional[str]] = mapped_column(String(100))
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
    
    job: Mapped[List['Job']] = relationship(
        'Job', 
        back_populates='material'
    )    

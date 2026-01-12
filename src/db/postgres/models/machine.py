from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import (
    BigInteger, DateTime, Double, ForeignKeyConstraint, Index, 
    PrimaryKeyConstraint, String, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Machine(Base):
    __tablename__ = 'myapp_machine'
    __table_args__ = (
        ForeignKeyConstraint(
            ['company_id'], 
            ['myapp_company.id'], 
            deferrable=True, 
            initially='DEFERRED', 
            name='myapp_machine_company_id_4d3a284a_fk_myapp_company_id'
        ),
        PrimaryKeyConstraint('id', name='myapp_machine_pkey'),
        Index('company_title', 'company_id', 'title'),
        Index('company_id', 'company_id'),
        Index('company_id_fk', 'company_id')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(600), nullable=False)
    machine_rigidity: Mapped[float] = mapped_column(Double(53), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    product_link: Mapped[Optional[str]] = mapped_column(String(200))
    price: Mapped[Optional[dict]] = mapped_column(JSONB)
    travels: Mapped[Optional[dict]] = mapped_column(JSONB)
    trunnion: Mapped[Optional[dict]] = mapped_column(JSONB)
    spindle: Mapped[Optional[dict]] = mapped_column(JSONB)
    b_axis_tilt: Mapped[Optional[dict]] = mapped_column(JSONB)
    c_axis_rotation: Mapped[Optional[dict]] = mapped_column(JSONB)
    feedrates: Mapped[Optional[dict]] = mapped_column(JSONB)
    tool_changer: Mapped[Optional[dict]] = mapped_column(JSONB)
    coolant_capacity: Mapped[Optional[dict]] = mapped_column(JSONB)
    air_requirements: Mapped[Optional[dict]] = mapped_column(JSONB)
    electrical_specification: Mapped[Optional[dict]] = mapped_column(JSONB)
    dimensions_shipping: Mapped[Optional[dict]] = mapped_column(JSONB)
    platter: Mapped[Optional[dict]] = mapped_column(JSONB)
    axis_motors: Mapped[Optional[dict]] = mapped_column(JSONB)
    table: Mapped[Optional[dict]] = mapped_column(JSONB)
    a_axis: Mapped[Optional[dict]] = mapped_column(JSONB)
    tapping: Mapped[Optional[dict]] = mapped_column(JSONB)
    axis: Mapped[Optional[int]] = mapped_column(BigInteger)
    company_id: Mapped[Optional[int]] = mapped_column(BigInteger)
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

    company: Mapped[Optional['Company']] = relationship(
        'Company', 
        back_populates='machine'
    )
    job: Mapped[List['Job']] = relationship(
        'Job', 
        back_populates='machine'
    )    
    stock: Mapped[List['Stock']] = relationship(
        'Stock', 
        back_populates='machine'
    )
    company_machine_mapping: Mapped[List['CompanyMachineMapping']] = relationship(
        'CompanyMachineMapping', 
        back_populates='machine'
    )
    
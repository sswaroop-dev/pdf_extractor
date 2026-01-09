from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, Float, ForeignKey, PrimaryKeyConstraint, String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ToolMaster(Base):
    __tablename__ = 'tool_master'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tool_master_pkey'),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[float] = mapped_column(Float(53), nullable=False)
    attributes: Mapped[dict] = mapped_column(JSONB, nullable=False)
    tool_taxonomy_code: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey('tool_taxonomy.code'),
        nullable=False
    )
    cutting_tool_material_taxonomy_code: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey('cutting_tool_taxonomy.code'),
        nullable=False
    )
    cutting_tool_coating_code: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey('cutting_tool_taxonomy.code'),
        nullable=False
    )
    vendor_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('myapp_vendor.id'),
        nullable=False
    )

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

    tool_taxonomy: Mapped['ToolTaxonomy'] = relationship(
        'ToolTaxonomy', 
        foreign_keys=[tool_taxonomy_code],
        back_populates='tool_master'
    )
    cutting_tool_material_taxonomy: Mapped['CuttingToolTaxonomy'] = relationship(
        'CuttingToolTaxonomy', 
        foreign_keys=[cutting_tool_material_taxonomy_code],
        back_populates='tool_master_material'
    )
    cutting_tool_coating_taxonomy: Mapped['CuttingToolTaxonomy'] = relationship(
        'CuttingToolTaxonomy', 
        foreign_keys=[cutting_tool_coating_code],
        back_populates='tool_master_coating'
    )
    vendor: Mapped['Vendor'] = relationship(
        'Vendor', 
        foreign_keys=[vendor_id],
        back_populates='tool_master'
    )
    company_tool_mapping: Mapped[list['CompanyToolMapping']] = relationship(
        'CompanyToolMapping', 
        foreign_keys='CompanyToolMapping.tool_master_id',
        back_populates='tool_master'
    )
    
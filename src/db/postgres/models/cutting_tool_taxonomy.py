from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Ltree, LtreeType

from .base import Base


class CuttingToolTaxonomy(Base):
    __tablename__ = 'cutting_tool_taxonomy'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='cutting_tool_taxonomy_pkey'),
    )

    code: Mapped[Ltree] = mapped_column(
        LtreeType, 
        primary_key=True,
        nullable=False
    )
    parent_code: Mapped[Optional[Ltree]] = mapped_column(
        LtreeType, 
        nullable=True
    )
    name: Mapped[str] = mapped_column(
        String(100), 
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

    tool_master_material: Mapped[list['ToolMaster']] = relationship(
        'ToolMaster', 
        foreign_keys='ToolMaster.cutting_tool_material_taxonomy_code',
        back_populates='cutting_tool_material_taxonomy'
    )
    tool_master_coating: Mapped[list['ToolMaster']] = relationship(
        'ToolMaster', 
        foreign_keys='ToolMaster.cutting_tool_coating_code',
        back_populates='cutting_tool_coating_taxonomy'
    )
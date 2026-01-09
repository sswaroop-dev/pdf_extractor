from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Ltree, LtreeType

from .base import Base


class ToolTaxonomy(Base):
    __tablename__ = 'tool_taxonomy'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='tool_taxonomy_pkey'),
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

    tool_attribute: Mapped[list['ToolAttribute']] = relationship(
        'ToolAttribute', 
        foreign_keys='ToolAttribute.tool_taxonomy_code',
        back_populates='tool_taxonomy'
    )
    tool_master: Mapped[list['ToolMaster']] = relationship(
        'ToolMaster', 
        foreign_keys='ToolMaster.tool_taxonomy_code',
        back_populates='tool_taxonomy'
    )
    default_policy_v2: Mapped[list['DefaultPolicyV2']] = relationship(
        'DefaultPolicyV2', 
        foreign_keys='DefaultPolicyV2.tool_taxonomy_code',
        back_populates='tool_taxonomy'
    )
    user_policy: Mapped[list['UserPolicy']] = relationship(
        'UserPolicy', 
        foreign_keys='UserPolicy.tool_taxonomy_code',
        back_populates='tool_taxonomy'
    )
    
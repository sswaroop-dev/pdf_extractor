from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint, String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ToolAttribute(Base):
    __tablename__ = 'tool_attribute'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tool_attribute_pkey'),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    tool_taxonomy_code: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey('tool_taxonomy.code'),
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
        back_populates='tool_attribute'
    )

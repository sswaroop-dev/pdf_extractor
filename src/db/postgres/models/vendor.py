from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, Index, PrimaryKeyConstraint, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Vendor(Base):
    __tablename__ = 'myapp_vendor'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='myapp_vendor_pkey'),
        UniqueConstraint('name', name='myapp_vendor_name_6566bff1_uniq'),
        Index('idx_vendor_name', 'name')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
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
    
    tool: Mapped[list['Tool']] = relationship('Tool', back_populates='vendor')
    tool_master: Mapped[list['ToolMaster']] = relationship(
        'ToolMaster', 
        foreign_keys='ToolMaster.vendor_id',
        back_populates='vendor'
    )

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    BigInteger, DateTime, Double, ForeignKeyConstraint, Index, Integer, 
    PrimaryKeyConstraint, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Tool(Base):
    __tablename__ = 'myapp_tool'
    __table_args__ = (
        ForeignKeyConstraint(['tool_type_id'], ['myapp_tooltype.id'], deferrable=True, initially='DEFERRED', name='myapp_tool_tool_type_id_f446a9eb_fk_myapp_tooltype_id'),
        ForeignKeyConstraint(['vendor_id'], ['myapp_vendor.id'], deferrable=True, initially='DEFERRED', name='myapp_tool_vendor_id_4982e751_fk_myapp_vendor_id'),
        PrimaryKeyConstraint('id', name='myapp_tool_pkey'),
        UniqueConstraint('product_id', name='myapp_tool_product_id_a8fde589_uniq'),
        Index('idx_tool_product_id', 'product_id'),
        Index('idx_tool_tool_type_id', 'tool_type_id'),
        Index('idx_tool_vendor_id', 'vendor_id')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    product_id: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tool_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    vendor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    material: Mapped[Optional[str]] = mapped_column(String(100))
    diameter: Mapped[Optional[float]] = mapped_column(Double(53))
    shank_diameter: Mapped[Optional[float]] = mapped_column(Double(53))
    cutting_length: Mapped[Optional[float]] = mapped_column(Double(53))
    flute_count: Mapped[Optional[int]] = mapped_column(Integer)
    body_length: Mapped[Optional[float]] = mapped_column(Double(53))
    corner_radius: Mapped[Optional[float]] = mapped_column(Double(53))
    overall_length: Mapped[Optional[float]] = mapped_column(Double(53))
    product_link: Mapped[Optional[str]] = mapped_column(String(200))
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

    tool_type: Mapped['ToolType'] = relationship(
        'ToolType', 
        back_populates='tool'
    )
    vendor: Mapped['Vendor'] = relationship('Vendor', back_populates='tool')
    company_tool_mapping: Mapped[List['CompanyToolMapping']] = relationship(
        'CompanyToolMapping', 
        back_populates='tool'
    )
    speed_and_feed: Mapped[list['SpeedAndFeed']] = relationship(
        'SpeedAndFeed', 
        back_populates='tool'
    )
    
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    BigInteger, DateTime, Double, ForeignKeyConstraint, Index, 
    PrimaryKeyConstraint, String, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base



class SpeedAndFeed(Base):
    __tablename__ = 'myapp_speedandfeedrate'
    __table_args__ = (
        ForeignKeyConstraint(['operation_id'], ['myapp_operation.id'], deferrable=True, initially='DEFERRED', name='myapp_speedandfeedra_operation_id_5f793f25_fk_myapp_ope'),
        ForeignKeyConstraint(['tool_id'], ['myapp_tool.id'], deferrable=True, initially='DEFERRED', name='myapp_speedandfeedrate_tool_id_20de7a37_fk_myapp_tool_id'),
        PrimaryKeyConstraint('id', name='myapp_speedandfeedrate_pkey'),
        UniqueConstraint('tool_id', 'material', 'operation_id', 'spindle_speed', 'preset_name', name='myapp_speedandfeedrate_tool_id_material_operati_6c14ccc3_uniq'),
        Index('idx_speed_feed_operation', 'operation_id'),
        Index('idx_speed_feed_tool', 'tool_id'),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    preset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    operation_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tool_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    material: Mapped[Optional[str]] = mapped_column(String(100))
    operation_notes: Mapped[Optional[str]] = mapped_column(Text)
    hardness_min_hb: Mapped[Optional[float]] = mapped_column(Double(53))
    hardness_max_hb: Mapped[Optional[float]] = mapped_column(Double(53))
    spindle_speed: Mapped[Optional[float]] = mapped_column(Double(53))
    surface_speed: Mapped[Optional[float]] = mapped_column(Double(53))
    cutting_feedrate: Mapped[Optional[float]] = mapped_column(Double(53))
    feed_per_tooth: Mapped[Optional[float]] = mapped_column(Double(53))
    stepdown: Mapped[Optional[float]] = mapped_column(Double(53))
    stepover: Mapped[Optional[float]] = mapped_column(Double(53))
    product_link: Mapped[Optional[str]] = mapped_column(String(500))
    plunge_feedrate: Mapped[Optional[float]] = mapped_column(Double(53))
    retract_feedrate: Mapped[Optional[float]] = mapped_column(Double(53))
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

    operation: Mapped['OperationName'] = relationship(
        'OperationName', 
        back_populates='speed_and_feed'
    )
    tool: Mapped['Tool'] = relationship(
        'Tool', 
        back_populates='speed_and_feed'
    )
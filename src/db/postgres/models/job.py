from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKeyConstraint, Index, 
    PrimaryKeyConstraint, String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Job(Base):
    __tablename__ = 'myapp_cadfeaturecache'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_cadfeaturecache_company_id_64c9b42b_fk_myapp_company_id'),
        ForeignKeyConstraint(['machine_id'], ['myapp_machine.id'], deferrable=True, initially='DEFERRED', name='myapp_cadfeaturecache_machine_id_bab2baac_fk_myapp_machine_id'),
        ForeignKeyConstraint(['material_id'], ['myapp_material.id'], deferrable=True, initially='DEFERRED', name='myapp_cadfeaturecache_material_id_7927354a_fk_myapp_material_id'),
        ForeignKeyConstraint(['stock_id'], ['myapp_stock.id'], deferrable=True, initially='DEFERRED', name='myapp_cadfeaturecache_stock_id_95c200c2_fk_myapp_stock_id'),
        ForeignKeyConstraint(['user_id'], ['myapp_user.id'], deferrable=True, initially='DEFERRED', name='myapp_cadfeaturecache_user_id_3c29bddd_fk_myapp_user_id'),
        PrimaryKeyConstraint('id', name='myapp_cadfeaturecache_pkey'),
        Index('idx_job_company_session', 'company_id', 'session_id'),    
        Index('idx_job_company', 'company_id'),                         
        Index('idx_job_session', 'session_id'),                         
        Index('idx_job_machine', 'machine_id'),                         
        Index('idx_job_material', 'material_id'),                       
        Index('idx_job_stock', 'stock_id'),                             
        Index('idx_job_user', 'user_id'),                               
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    features: Mapped[dict] = mapped_column(JSONB, nullable=False)
    bounding_box: Mapped[dict] = mapped_column(JSONB, nullable=False)
    directions: Mapped[list] = mapped_column(JSONB, nullable=False)
    deterministic_completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    ai_strategy_completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    operations_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    operations_json_v2: Mapped[dict] = mapped_column(JSONB, nullable=False)
    flagged_features: Mapped[dict] = mapped_column(JSONB, nullable=False)
    session_id: Mapped[Optional[str]] = mapped_column(String(128))
    machine_rigidity: Mapped[Optional[str]] = mapped_column(String(20))
    machine_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    material_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    stock_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    company_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ratings_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    cad_url: Mapped[Optional[str]] = mapped_column(String(255))
    glb_map_url: Mapped[Optional[str]] = mapped_column(String(255))
    glb_url: Mapped[Optional[str]] = mapped_column(String(255))
    policy: Mapped[Optional[dict]] = mapped_column(JSONB)
    gdt_url: Mapped[Optional[str]] = mapped_column(String(255))
    gdt_cache_url: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
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
        back_populates='job'
    )
    machine: Mapped[Optional['Machine']] = relationship(
        'Machine', back_populates='job'
    )
    material: Mapped[Optional['Material']] = relationship(
        'Material', back_populates='job'
    )
    stock: Mapped[Optional['Stock']] = relationship(
        'Stock', back_populates='job'
    )
    user: Mapped[Optional['User']] = relationship(
        'User', back_populates='job'
    )
    machine_operation_plan: Mapped[Optional['MachineOperationPlan']] = relationship(
        'MachineOperationPlan', back_populates='job'
    )
    formatted_feature: Mapped[Optional['FormattedFeature']] = relationship(
        'FormattedFeature', 
        back_populates='job'
    )
    user_feedback: Mapped[Optional['UserFeedback']] = relationship(
        'UserFeedback', back_populates='job'
    )

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    ARRAY, BigInteger, DateTime, ForeignKeyConstraint, Index, Integer, 
    PrimaryKeyConstraint, String, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FormattedFeature(Base):
    __tablename__ = 'myapp_formattedfeature'
    __table_args__ = (
        ForeignKeyConstraint(['cad_feature_cache_id'], ['myapp_cadfeaturecache.id'], deferrable=True, initially='DEFERRED', name='myapp_formattedfeatu_cad_feature_cache_id_0da3c130_fk_myapp_cad'),
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_formattedfeature_company_id_e3305f0f_fk_myapp_company_id'),
        PrimaryKeyConstraint('id', name='myapp_formattedfeature_pkey'),
        Index('idx_formattedfeature_company_feature', 'company_id', 'feature_id'),
        Index('idx_formattedfeature_company', 'company_id'),
        Index('idx_formattedfeature_feature_id', 'feature_id'),
        Index('idx_formattedfeature_feature_type_index', 'feature_type', 'index'),
        Index('idx_formattedfeature_job', 'cad_feature_cache_id'),
        Index('idx_formattedfeature_feature_id_like', 'feature_id'),
        Index('idx_formattedfeature_feature_type', 'feature_type'),
        Index('idx_formattedfeature_feature_type_like', 'feature_type'),
        Index('idx_formattedfeature_index', 'index')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    feature_type: Mapped[str] = mapped_column(String(64), nullable=False)
    faces: Mapped[dict] = mapped_column(JSONB, nullable=False)
    dimensions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    directions: Mapped[list[dict[str, float]]] = mapped_column(
        ARRAY(JSONB), 
        nullable=False
    )
    bounding_box: Mapped[dict] = mapped_column(JSONB, nullable=False)
    triangle_indices: Mapped[list[int]] = mapped_column(
        ARRAY(Integer()), 
        nullable=False
    )
    manufacturing_notes: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), 
        nullable=False
    )
    required_ops: Mapped[list[str]] = mapped_column(
        ARRAY(String(length=64)), 
        nullable=False
    )
    optional_ops: Mapped[list[str]] = mapped_column(
        ARRAY(String(length=64)), 
        nullable=False
    )
    face_indices: Mapped[list[int]] = mapped_column(
        ARRAY(Integer()), 
        nullable=False
    )
    feature_id: Mapped[Optional[str]] = mapped_column(String(40))
    index: Mapped[Optional[int]] = mapped_column(Integer)
    company_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    adjacent_planes: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String(length=64))
    )
    cad_feature_cache_id: Mapped[Optional[int]] = mapped_column(BigInteger)
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

    job: Mapped[Optional['Job']] = relationship(
        'Job', 
        back_populates='formatted_feature'
    )
    company: Mapped[Optional['Company']] = relationship(
        'Company', 
        back_populates='formatted_feature'
    )

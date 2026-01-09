from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, ForeignKey, ForeignKeyConstraint, Index, 
    PrimaryKeyConstraint, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CompanyToolMapping(Base):
    __tablename__ = 'myapp_companytoolmapping'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_companytoolmap_company_id_f7c459ac_fk_myapp_com'),
        ForeignKeyConstraint(['tool_id'], ['myapp_tool.id'], deferrable=True, initially='DEFERRED', name='myapp_companytoolmapping_tool_id_fc5afe96_fk_myapp_tool_id'),
        PrimaryKeyConstraint('id', name='myapp_companytoolmapping_pkey'),
        UniqueConstraint('company_id', 'tool_id', name='unique_company_tool_mapping'),
        Index('idx_company_tool_mapping_company_tool', 'company_id', 'tool_id'),
        Index('idx_company_tool_mapping_tool_id', 'tool_id'),
        Index('idx_company_tool_mapping_company', 'company_id'),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    company_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tool_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tool_master_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('tool_master.id'),
        nullable=True
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

    company: Mapped['Company'] = relationship(
        'Company', 
        back_populates='company_tool_mapping'
    )
    tool: Mapped['Tool'] = relationship(
        'Tool', 
        back_populates='company_tool_mapping'
    )
    tool_master: Mapped['ToolMaster'] = relationship(
        'ToolMaster', 
        foreign_keys=[tool_master_id],
        back_populates='company_tool_mapping'
    )

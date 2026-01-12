from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, ForeignKeyConstraint, Index, PrimaryKeyConstraint, 
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CompanyMachineMapping(Base):
    __tablename__ = 'myapp_companymachinemapping'
    __table_args__ = (
        ForeignKeyConstraint(['added_by_id'], ['myapp_user.id'], deferrable=True, initially='DEFERRED', name='myapp_companymachine_added_by_id_572fb21a_fk_myapp_use'),
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_companymachine_company_id_55c6568b_fk_myapp_com'),
        ForeignKeyConstraint(['machine_id'], ['myapp_machine.id'], deferrable=True, initially='DEFERRED', name='myapp_companymachine_machine_id_21a43cbb_fk_myapp_mac'),
        PrimaryKeyConstraint('id', name='myapp_companymachinemapping_pkey'),
        UniqueConstraint('company_id', 'machine_id', name='unique_company_machine_mapping'),
        Index('idx_cmm_company_machine', 'company_id', 'machine_id'),
        Index('idx_cmm_added_by', 'added_by_id'), 
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )
    company_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    machine_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    added_by_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
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

    added_by: Mapped['User'] = relationship(
        'User', 
        back_populates='company_machine_mapping'
    )
    company: Mapped['Company'] = relationship(
        'Company', 
        back_populates='company_machine_mapping'
    )
    machine: Mapped['Machine'] = relationship(
        'Machine', 
        back_populates='company_machine_mapping'
    )

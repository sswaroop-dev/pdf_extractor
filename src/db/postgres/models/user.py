from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKeyConstraint, Index, 
    PrimaryKeyConstraint, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'myapp_user'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_user_company_id_315cca42_fk_myapp_company_id'),
        ForeignKeyConstraint(['role_id'], ['myapp_userrole.id'], deferrable=True, initially='DEFERRED', name='myapp_user_role_id_23830f6e_fk_myapp_userrole_id'),
        PrimaryKeyConstraint('id', name='myapp_user_pkey'),
        UniqueConstraint('email', name='myapp_user_email_key'),
        Index('idx_user_company', 'company_id'),                   
        Index('idx_user_email', 'email'),                          
        Index('idx_user_email_like', 'email'),                     
        Index('idx_user_role', 'role_id'),                         
        Index('idx_user_company_role', 'company_id', 'role_id'),   
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    company_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(17))
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

    company: Mapped['Company'] = relationship('Company', back_populates='user')
    role: Mapped['UserRole'] = relationship('UserRole', back_populates='user')
    job: Mapped[List['Job']] = relationship(
        'Job', 
        back_populates='user'
    ) 
    company_machine_mapping: Mapped[List['CompanyMachineMapping']] = relationship(
        'CompanyMachineMapping', 
        back_populates='added_by'
    )
    invitation: Mapped[list['Invitation']] = relationship(
        'Invitation', 
        back_populates='invited_by'
    )
    user_feedback: Mapped[List['UserFeedback']] = relationship(
        'UserFeedback', 
        back_populates='user'
    )
    user_policy: Mapped[list['UserPolicy']] = relationship(
        'UserPolicy',
        foreign_keys='UserPolicy.user_id',
        back_populates='user'
    )
    user_default_policy_exclusions: Mapped[list['UserDefaultPolicyExclusion']] = relationship(
        'UserDefaultPolicyExclusion',
        foreign_keys='UserDefaultPolicyExclusion.user_id',
        back_populates='user',
    )
    
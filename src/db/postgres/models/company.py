from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, DateTime, Index, Integer, 
    PrimaryKeyConstraint, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Company(Base):
    __tablename__ = 'myapp_company'
    __table_args__ = (
        CheckConstraint('employee_count >= 0', name='myapp_company_employee_count_check'),
        PrimaryKeyConstraint('id', name='myapp_company_pkey'),
        UniqueConstraint('name', name='myapp_company_name_key'),
        UniqueConstraint('slug', name='myapp_company_slug_key'),
        Index('idx_company_is_active', 'is_active'),
        Index('idx_company_slug', 'slug'),
        Index('idx_company_name_like', 'name'),
        Index('idx_company_slug_like', 'slug')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    default_units: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(254))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    website: Mapped[Optional[str]] = mapped_column(String(200))
    address_line_1: Mapped[Optional[str]] = mapped_column(String(255))
    address_line_2: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state_province: Mapped[Optional[str]] = mapped_column(String(100))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    employee_count: Mapped[Optional[int]] = mapped_column(Integer)
    annual_revenue: Mapped[Optional[str]] = mapped_column(String(50))
    license_key: Mapped[Optional[str]] = mapped_column(String(100))
    max_jobs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_machines: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_users: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
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
    
    machine: Mapped[List['Machine']] = relationship(
        'Machine', 
        back_populates='company'
    )
    user: Mapped[List['User']] = relationship(
        'User', 
        back_populates='company'
    )
    job: Mapped[List['Job']] = relationship(
        'Job', 
        back_populates='company'
    )
    company_machine_mapping: Mapped[List['CompanyMachineMapping']] = relationship(
        'CompanyMachineMapping', 
        back_populates='company'
    )
    company_tool_mapping: Mapped[List['CompanyToolMapping']] = relationship(
        'CompanyToolMapping', 
        back_populates='company'
    )
    formatted_feature: Mapped[List['FormattedFeature']] = relationship(
        'FormattedFeature', 
        back_populates='company'
    )
    invitation: Mapped[List['Invitation']] = relationship(
        'Invitation', 
        back_populates='company'
    )
    user_feedback: Mapped[List['UserFeedback']] = relationship(
        'UserFeedback', 
        back_populates='company'
    )

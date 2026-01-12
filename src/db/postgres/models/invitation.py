from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKeyConstraint, Identity, Index, 
    PrimaryKeyConstraint, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Invitation(Base):
    __tablename__ = 'myapp_invitation'
    __table_args__ = (
        ForeignKeyConstraint(['invited_by_id'], ['myapp_user.id'], deferrable=True, initially='DEFERRED', name='myapp_invitation_invited_by_id_38859190_fk_myapp_user_id'),
        ForeignKeyConstraint(['role_id'], ['myapp_userrole.id'], deferrable=True, initially='DEFERRED', name='myapp_invitation_role_id_01114e9e_fk_myapp_userrole_id'),
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_invitation_company_id_cfb4286b_fk_myapp_company_id'),
        PrimaryKeyConstraint('id', name='myapp_invitation_pkey'),
        UniqueConstraint('token', name='myapp_invitation_token_key'),
        Index('idx_invitation_invited_by', 'invited_by_id'),
        Index('idx_invitation_role', 'role_id'),
        Index('idx_invitation_token', 'token')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    token: Mapped[str] = mapped_column(String(100), nullable=False)
    invited_by_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    company_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
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

    invited_by: Mapped['User'] = relationship(
        'User', 
        back_populates='invitation'
    )
    role: Mapped['UserRole'] = relationship(
        'UserRole', 
        back_populates='invitation'
    )
    company: Mapped['Company'] = relationship(
        'Company', 
        back_populates='invitation'
    )

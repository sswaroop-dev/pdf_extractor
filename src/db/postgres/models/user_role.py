from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, Index, PrimaryKeyConstraint, String, 
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserRole(Base):
    __tablename__ = 'myapp_userrole'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='myapp_userrole_pkey'),
        UniqueConstraint('name', name='myapp_userrole_name_key'),
        Index('idx_userrole_name', 'name')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
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

    user: Mapped[list['User']] = relationship('User', back_populates='role')
    invitation: Mapped[list['Invitation']] = relationship(
        'Invitation', 
        back_populates='role'
    )
    
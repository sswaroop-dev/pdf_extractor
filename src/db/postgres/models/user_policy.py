from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint, String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import LtreeType, Ltree

from .base import Base


class UserPolicy(Base):
    """
    User-specific machining policy overrides.
    
    This table lets a user add or adjust policy candidates for a given
    operation + policy tier (ideal / moderate / worst), optionally scoped
    to a material category.
    """
    __tablename__ = "user_policy"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_policy_pkey"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    tier: Mapped[str] = mapped_column(String(16), nullable=False)
    applies_if: Mapped[dict] = mapped_column(JSONB, nullable=False)
    constraints: Mapped[dict] = mapped_column(JSONB, nullable=False)
    preferences: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('myapp_user.id'),
        nullable=False,
    )
    tool_taxonomy_code: Mapped[Ltree] = mapped_column(
        LtreeType, 
        ForeignKey('tool_taxonomy.code'),
        nullable=False
    )
    operation_id = mapped_column(
        BigInteger,
        ForeignKey('myapp_operation.id'),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        nullable=False,
        default=datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        nullable=True,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='user_policy',
    )
    tool_taxonomy: Mapped['ToolTaxonomy'] = relationship(
        'ToolTaxonomy', 
        foreign_keys=[tool_taxonomy_code],
        back_populates='user_policy'
    )
    operation: Mapped['OperationName'] = relationship(
        'OperationName',
        foreign_keys=[operation_id],
        back_populates='user_policy',
    )

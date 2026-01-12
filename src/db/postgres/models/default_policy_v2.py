from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, ForeignKey, PrimaryKeyConstraint, String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Ltree, LtreeType

from .base import Base


class DefaultPolicyV2(Base):
    """
    Default machining policy candidates loaded from JSON configs.
    
    These are the baseline policies that all users start with.
    Users can disable specific default policies via DisabledDefaultPolicy.
    """
    __tablename__ = "default_policy_v2"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="default_policy_v2_pkey"),
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

    tool_taxonomy: Mapped['ToolTaxonomy'] = relationship(
        'ToolTaxonomy', 
        foreign_keys=[tool_taxonomy_code],
        back_populates='default_policy_v2'
    )
    operation: Mapped['OperationName'] = relationship(
        'OperationName',
        foreign_keys=[operation_id],
        back_populates='default_policy_v2',
    )
    user_default_policy_exclusions: Mapped[list['UserDefaultPolicyExclusion']] = relationship(
        'UserDefaultPolicyExclusion',
        foreign_keys='UserDefaultPolicyExclusion.default_policy_id',
        back_populates='default_policy',
    )
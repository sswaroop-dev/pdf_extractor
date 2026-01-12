from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PolicyOverride(Base):
    """
    User-specific overrides for machining policy candidates.

    This table lets a user add or adjust policy candidates for a given
    operation + policy tier (ideal / moderate / worst), optionally scoped
    to a material category.
    """

    # NOTE: Table name matches the Django model `PolicyOverride` in `myapp.models`,
    # which will create the table `myapp_policyoverride` via migrations.
    __tablename__ = "myapp_policyoverride"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["myapp_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="policy_overrides_user_id_fk_myapp_user_id",
        ),
        PrimaryKeyConstraint("id", name="policy_overrides_pkey"),
        Index("idx_policy_overrides_user_operation", "user_id", "operation"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # Owning user
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Operation name this override applies to (e.g. "drilling", "roughing")
    operation: Mapped[str] = mapped_column(String(64), nullable=False)

    # Policy tier this override belongs to: "ideal" | "moderate" | "worst"
    policy_tier: Mapped[str] = mapped_column(String(16), nullable=False)

    # Optional material category filter: "soft" | "medium" | "tough", or None for all
    material_category: Mapped[Optional[str]] = mapped_column(String(32))

    # Tool type information
    tool_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tool_type_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Constraints JSON, same shape as config/policy/*.json "constraints" blocks
    constraints: Mapped[dict] = mapped_column(JSONB, nullable=False)

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


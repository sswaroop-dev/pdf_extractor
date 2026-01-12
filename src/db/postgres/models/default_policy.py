from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Index, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DefaultPolicy(Base):
    """
    Default machining policy candidates loaded from JSON configs.
    
    These are the baseline policies that all users start with.
    Users can disable specific default policies via DisabledDefaultPolicy.
    """

    # NOTE: Table name matches the Django model `DefaultPolicy` in `myapp.models`,
    # which will create the table `myapp_defaultpolicy` via migrations.
    __tablename__ = "myapp_defaultpolicy"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="default_policy_pkey"),
        Index("idx_default_policy_operation_tier", "operation", "policy_tier"),
        Index("idx_default_policy_policy_id", "policy_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # Operation name (e.g. "drilling", "roughing")
    operation: Mapped[str] = mapped_column(String(64), nullable=False)

    # Policy tier: "ideal" | "moderate" | "worst"
    policy_tier: Mapped[str] = mapped_column(String(16), nullable=False)

    # Optional material category: "soft" | "medium" | "tough" or None for all
    material_category: Mapped[Optional[str]] = mapped_column(String(32))

    # Tool type information
    tool_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tool_type_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Constraints JSON, same shape as config/policy/*.json "constraints" blocks
    constraints: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Unique identifier for this policy (used for disabling)
    # Format: {operation}_{tier}_{tool_type_id}_{material}[_{feature_type|_surface_type}]
    policy_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

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


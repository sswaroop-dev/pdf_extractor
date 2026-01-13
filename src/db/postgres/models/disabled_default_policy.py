from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Index, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DisabledDefaultPolicy(Base):
    """
    Maps users to disabled default policies.
    
    When a user disables a default policy, a record is created here.
    This allows users to selectively disable default policies they don't want to use.
    """

    # NOTE: Table name matches the Django model `DisabledDefaultPolicy` in `myapp.models`,
    # which will create the table `myapp_disableddefaultpolicy` via migrations.
    __tablename__ = "myapp_disableddefaultpolicy"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["myapp_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="disabled_default_policies_user_id_fk_myapp_user_id",
        ),
        PrimaryKeyConstraint("id", name="disabled_default_policies_pkey"),
        Index("idx_disabled_default_policies_user_policy", "user_id", "policy_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # Owning user
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Reference to the default policy via policy_id
    policy_id: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        nullable=False,
        default=datetime.now(timezone.utc),
    )


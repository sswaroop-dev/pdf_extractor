from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint, 
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserDefaultPolicyExclusion(Base):
    """
    Maps users to disabled default policies.
    
    When a user disables a default policy, a record is created here.
    This allows users to selectively disable default policies they don't want to use.
    """
    __tablename__ = "user_default_policy_exclusion"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_default_policy_exclusion_pkey"),
        UniqueConstraint(
            "user_id", 
            "default_policy_id", 
            name="uq_user_default_policy_exclusion"
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('myapp_user.id'), 
        nullable=False
    )
    default_policy_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('default_policy_v2.id'), 
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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
        back_populates='user_default_policy_exclusions',
    )
    default_policy: Mapped['DefaultPolicyV2'] = relationship(
        'DefaultPolicyV2',
        foreign_keys=[default_policy_id],
        back_populates='user_default_policy_exclusions',
    )


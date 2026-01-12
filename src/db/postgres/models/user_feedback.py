from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, DateTime, ForeignKeyConstraint, Index, PrimaryKeyConstraint, 
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserFeedback(Base):
    __tablename__ = 'myapp_userfeedback'
    __table_args__ = (
        ForeignKeyConstraint(['cad_feature_cache_id'], ['myapp_cadfeaturecache.id'], deferrable=True, initially='DEFERRED', name='myapp_userfeedback_cad_feature_cache_id_f10c3c1e_fk_myapp_cad'),
        ForeignKeyConstraint(['company_id'], ['myapp_company.id'], deferrable=True, initially='DEFERRED', name='myapp_userfeedback_company_id_67866f17_fk_myapp_company_id'),
        ForeignKeyConstraint(['user_id'], ['myapp_user.id'], deferrable=True, initially='DEFERRED', name='myapp_userfeedback_user_id_201fbf09_fk_myapp_user_id'),
        PrimaryKeyConstraint('id', name='myapp_userfeedback_pkey'),
        Index('idx_user_feedback_cad_feature_cache', 'cad_feature_cache_id'),
        Index('idx_user_feedback_company', 'company_id'),
        Index('idx_user_feedback_user', 'user_id')
    )

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    cad_feature_cache_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    company_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
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

    job: Mapped['Job'] = relationship('Job', back_populates='user_feedback')
    company: Mapped['Company'] = relationship('Company', back_populates='user_feedback')
    user: Mapped['User'] = relationship('User', back_populates='user_feedback')

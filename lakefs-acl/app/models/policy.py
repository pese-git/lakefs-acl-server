import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base, group_policy, user_policy


class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    document = Column(String, nullable=False)  # JSON blob or similar
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    users = relationship("User", secondary=user_policy, back_populates="policies")
    groups = relationship("Group", secondary=group_policy, back_populates="policies")

import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base, group_policy, user_group


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, unique=True, nullable=False, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    users = relationship("User", secondary=user_group, back_populates="groups")
    policies = relationship("Policy", secondary=group_policy, back_populates="groups")

import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True)
    access_key = Column(String, unique=True, nullable=False, index=True)
    secret_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    user = relationship("User", back_populates="credentials")

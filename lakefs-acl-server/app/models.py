import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association tables
user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

group_policy = Table(
    "group_policy",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("policy_id", ForeignKey("policies.id"), primary_key=True),
)

user_policy = Table(
    "user_policy",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("policy_id", ForeignKey("policies.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    groups = relationship("Group", secondary=user_group, back_populates="users")
    policies = relationship("Policy", secondary=user_policy, back_populates="users")
    credentials = relationship("Credential", back_populates="user")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    users = relationship("User", secondary=user_group, back_populates="groups")
    policies = relationship("Policy", secondary=group_policy, back_populates="groups")


class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    document = Column(String, nullable=False)  # JSON blob or similar
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    users = relationship("User", secondary=user_policy, back_populates="policies")
    groups = relationship("Group", secondary=group_policy, back_populates="policies")


class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True)
    access_key = Column(String, unique=True, nullable=False, index=True)
    secret_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="credentials")

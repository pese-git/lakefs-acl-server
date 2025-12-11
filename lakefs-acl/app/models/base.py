from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Association tables (shared)
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

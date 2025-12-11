from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.group import GroupRead
from app.schemas.user import UserRead


class PolicyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    document: str


class PolicyCreate(PolicyBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "readonly",
                "document": '{"effect": "allow", "actions": ["read"]}'
            }
        }


class PolicyRead(PolicyBase):
    id: int
    users: Optional[List[UserRead]] = []
    groups: Optional[List[GroupRead]] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "readonly",
                "document": '{"effect": "allow", "actions": ["read"]}',
                "users": [
                    {"id": 1, "username": "john_doe", "email": "john@example.com", "is_active": True}
                ],
                "groups": [
                    {"id": 1, "name": "admins"}
                ]
            }
        }

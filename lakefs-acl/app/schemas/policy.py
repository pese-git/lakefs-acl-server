from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.user import UserRead
from app.schemas.group import GroupRead

class PolicyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    document: str

class PolicyCreate(PolicyBase):
    pass

class PolicyRead(PolicyBase):
    id: int
    users: Optional[List[UserRead]] = []
    groups: Optional[List[GroupRead]] = []
    class Config:
        from_attributes = True

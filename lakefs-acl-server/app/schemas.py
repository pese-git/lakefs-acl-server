from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- User Schemas ---

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    class Config:
        from_attributes = True
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# --- User Schemas ---


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": True
            }
        }

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": True
            }
        }

class UserListResponse(BaseModel):
    results: list[UserRead]
    # Если lakeFS потребуется amount:
    # amount: int

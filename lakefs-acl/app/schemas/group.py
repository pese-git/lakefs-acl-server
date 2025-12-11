from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class GroupCreate(GroupBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "admins"
            }
        }

class GroupRead(GroupBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "admins"
            }
        }

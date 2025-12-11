from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: int

    class Config:
        from_attributes = True

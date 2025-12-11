from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class GroupCreate(GroupBase):
    class Config:
        json_schema_extra = {"example": {"name": "admins"}}


class GroupRead(GroupBase):
    class Config:
        from_attributes = True
        json_schema_extra = {"example": {"id": "1", "name": "admins"}}

    # @classmethod
    # def from_orm(cls, obj):
    #    data = obj.__dict__.copy()
    #    data["id"] = str(obj.id)
    #    return cls(**data)

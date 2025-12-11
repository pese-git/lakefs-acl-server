from pydantic import BaseModel, Field


class PolicyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    document: str


class PolicyCreate(PolicyBase):
    pass


class PolicyRead(PolicyBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field


class CredentialBase(BaseModel):
    access_key: str = Field(..., min_length=3, max_length=255)
    secret_key: str = Field(..., min_length=3, max_length=255)
    user_id: int


class CredentialCreate(CredentialBase):
    pass


class CredentialRead(CredentialBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel


class CredentialCreate(BaseModel):
    access_key: str
    secret_key: str
    user_id: int


class CredentialRead(BaseModel):
    id: int
    access_key: str
    secret_key: str
    user_id: int

    class Config:
        from_attributes = True

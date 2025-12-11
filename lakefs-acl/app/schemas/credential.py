from pydantic import BaseModel


class CredentialCreate(BaseModel):
    access_key: str
    secret_key: str
    user_id: int
    class Config:
        json_schema_extra = {
            "example": {
                "access_key": "X6hqbnLMhJ1Fz3PO",
                "secret_key": "rNcVLzF8Gq6KzmQ64rE9tPoNXoMYiXQlEJH0Lm7R",
                "user_id": 1
            }
        }


class CredentialRead(BaseModel):
    id: int
    access_key: str
    secret_key: str
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 10,
                "access_key": "X6hqbnLMhJ1Fz3PO",
                "secret_key": "rNcVLzF8Gq6KzmQ64rE9tPoNXoMYiXQlEJH0Lm7R",
                "user_id": 1
            }
        }

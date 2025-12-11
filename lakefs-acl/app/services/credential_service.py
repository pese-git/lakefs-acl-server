from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.credential_repository import CredentialRepository
from app.schemas.credential import CredentialCreate


class CredentialService:
    def __init__(self, db: Session):
        self.repo = CredentialRepository(db)

    def create_credential(self, credential_data: CredentialCreate):
        if self.repo.get_by_access_key(credential_data.access_key):
            raise HTTPException(status_code=409, detail="Access key already exists")
        return self.repo.create(credential_data)

    def get_credential(self, credential_id: int):
        cred = self.repo.get_by_id(credential_id)
        if not cred:
            raise HTTPException(status_code=404, detail="Credential not found")
        return cred

    def list_credentials(self):
        return self.repo.list_all()

    def delete_credential(self, credential_id: int):
        cred = self.repo.get_by_id(credential_id)
        if not cred:
            raise HTTPException(status_code=404, detail="Credential not found")
        self.repo.delete(cred)
        return None

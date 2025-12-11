import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.credential_repository import CredentialRepository


class CredentialService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CredentialRepository(db)

    # --- Новый функционал для пользователя ---
    def create_credential_for_user(self, user_id: int):
        from app.repositories.user_repository import UserRepository

        user_repo = UserRepository(self.db)
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        access_key = secrets.token_urlsafe(16)
        secret_key = secrets.token_urlsafe(32)
        # Можно сделать проверку уникальности access_key на более сложной БД
        cred = self.repo.create_for_user(user_id, access_key, secret_key)
        return cred

    def list_user_credentials(self, user_id: int):
        return self.repo.list_by_user_id(user_id)

    def get_user_credential(self, user_id: int, credential_id: int):
        cred = self.repo.get_by_id(credential_id)
        if not cred or cred.user_id != user_id:
            raise HTTPException(status_code=404, detail="Credential not found")
        return cred

    def delete_user_credential(self, user_id: int, credential_id: int):
        cred = self.repo.get_by_id(credential_id)
        if not cred or cred.user_id != user_id:
            raise HTTPException(status_code=404, detail="Credential not found")
        self.repo.delete(cred)
        return None

    def get_credential_by_access_key(self, access_key: str):
        cred = self.repo.get_by_access_key(access_key)
        if not cred:
            raise HTTPException(status_code=404, detail="Credential not found")
        return cred

    # Оставим старые базовые методы для обратной совместимости (если нужно)
    def create_credential(self, credential_data):
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

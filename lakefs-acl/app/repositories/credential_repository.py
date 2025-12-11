from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.credential import Credential
from app.schemas.credential import CredentialCreate


class CredentialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_access_key(self, access_key: str) -> Optional[Credential]:
        return self.db.query(Credential).filter(Credential.access_key == access_key).first()

    def get_by_id(self, credential_id: int) -> Optional[Credential]:
        return self.db.query(Credential).filter(Credential.id == credential_id).first()

    def create(self, credential_data: CredentialCreate) -> Credential:
        cred = Credential(
            access_key=credential_data.access_key,
            secret_key=credential_data.secret_key,
            user_id=credential_data.user_id,
        )
        self.db.add(cred)
        self.db.commit()
        self.db.refresh(cred)
        return cred

    def list_all(self) -> List[Credential]:
        return self.db.query(Credential).all()

    def delete(self, cred: Credential):
        self.db.delete(cred)
        self.db.commit()

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.credential import CredentialRead
from app.services.credential_service import CredentialService

router = APIRouter(tags=["Credentials"])


# --- CRUD для credentials, вложенные в user ---
@router.post(
    "/auth/users/{user_id}/credentials",
    response_model=CredentialRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user_credential(user_id: int, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.create_credential_for_user(user_id)


@router.get("/auth/users/{user_id}/credentials", response_model=list[CredentialRead])
def list_user_credentials(user_id: int, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.list_user_credentials(user_id)


@router.get("/auth/users/{user_id}/credentials/{credential_id}", response_model=CredentialRead)
def get_user_credential(user_id: int, credential_id: int, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.get_user_credential(user_id, credential_id)


@router.delete(
    "/auth/users/{user_id}/credentials/{credential_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_credential(user_id: int, credential_id: int, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.delete_user_credential(user_id, credential_id)


# --- Для интеграции с lakeFS ---
@router.get("/auth/credentials/{access_key}", response_model=CredentialRead)
def get_credential_by_access_key(access_key: str, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.get_credential_by_access_key(access_key)

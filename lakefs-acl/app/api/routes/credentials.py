from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.credential import CredentialCreate, CredentialRead
from app.services.credential_service import CredentialService

router = APIRouter(prefix="/credentials", tags=["Credentials"])


@router.post("/", response_model=CredentialRead, status_code=status.HTTP_201_CREATED)
def create_credential(cred: CredentialCreate, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.create_credential(cred)


@router.get("/", response_model=list[CredentialRead])
def list_credentials(db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.list_credentials()


@router.get("/{credential_id}", response_model=CredentialRead)
def get_credential(credential_id: int, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.get_credential(credential_id)


@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credential(credential_id: int, db: Session = Depends(get_db)):
    service = CredentialService(db)
    return service.delete_credential(credential_id)

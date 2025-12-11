from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.policy import PolicyCreate, PolicyRead
from app.services.policy_service import PolicyService

router = APIRouter(prefix="/policies", tags=["Policies"])


@router.post("/", response_model=PolicyRead, status_code=status.HTTP_201_CREATED)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    service = PolicyService(db)
    return service.create_policy(policy)


@router.get("/", response_model=list[PolicyRead])
def list_policies(db: Session = Depends(get_db)):
    service = PolicyService(db)
    return service.list_policies()


@router.get("/{policy_id}", response_model=PolicyRead)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    service = PolicyService(db)
    return service.get_policy(policy_id)


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    service = PolicyService(db)
    return service.delete_policy(policy_id)

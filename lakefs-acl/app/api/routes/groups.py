from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.group import GroupCreate, GroupRead
from app.services.group_service import GroupService

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.create_group(group)


@router.get("/", response_model=list[GroupRead])
def list_groups(db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.list_groups()


@router.get("/{group_id}", response_model=GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_group(group_id)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.delete_group(group_id)

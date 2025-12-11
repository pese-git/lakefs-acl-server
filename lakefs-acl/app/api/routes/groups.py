from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.group import GroupCreate, GroupRead
from app.services.group_service import GroupService

router = APIRouter(prefix="/auth/groups", tags=["Groups"])


@router.post("/", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.create_group(group)


@router.get("/", response_model=list[GroupRead])
def list_groups(db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.list_groups()


@router.get("/{group_id}", response_model=GroupRead)
def get_group(group_id: str, db: Session = Depends(get_db)):
    service = GroupService(db)

    return service.get_group_by_name(group_id)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: str, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.delete_group(group_id)


# --- Новый функционал: управление членством ---
from app.schemas.user import UserRead


@router.put(
    "/{group_id}/members/{user_id}", response_model=GroupRead, status_code=status.HTTP_201_CREATED
)
def add_user_to_group(group_id: str, user_id: str, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.add_user_to_group(group_id, user_id)


@router.delete("/{group_id}/members/{user_id}", response_model=GroupRead)
def remove_user_from_group(group_id: str, user_id: str, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.remove_user_from_group(group_id, user_id)


@router.get("/{group_id}/members", response_model=list[UserRead])
def get_group_members(group_id: str, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_group_members(group_id)

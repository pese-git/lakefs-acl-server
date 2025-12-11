from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.group_repository import GroupRepository
from app.schemas.group import GroupCreate


class GroupService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = GroupRepository(db)

    def create_group(self, group_data: GroupCreate):
        if self.repo.get_by_name(group_data.name):
            raise HTTPException(status_code=409, detail="Group already exists")
        return self.repo.create(group_data)

    def get_group(self, group_id: int):
        group = self.repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group

    def list_groups(self):
        return self.repo.list_all()

    def delete_group(self, group_id: int):
        group = self.repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        self.repo.delete(group)
        return None

    # --- Новый функционал для членства ---
    def add_user_to_group(self, group_id: int, user_id: int):
        from app.repositories.user_repository import UserRepository

        user_repo = UserRepository(self.db)
        group = self.repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repo.add_user_to_group(group, user)

    def remove_user_from_group(self, group_id: int, user_id: int):
        from app.repositories.user_repository import UserRepository

        user_repo = UserRepository(self.db)
        group = self.repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repo.remove_user_from_group(group, user)

    def get_group_members(self, group_id: int):
        group = self.repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return self.repo.get_group_members(group)

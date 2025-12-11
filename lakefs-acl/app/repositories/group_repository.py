from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.group import Group
from app.schemas.group import GroupCreate


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Group]:
        return self.db.query(Group).filter(Group.name == name).first()

    def get_by_id(self, group_id: int) -> Optional[Group]:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def create(self, group_data: GroupCreate) -> Group:
        group = Group(name=group_data.name)
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def list_all(self) -> List[Group]:
        return self.db.query(Group).all()

    def delete(self, group: Group):
        self.db.delete(group)
        self.db.commit()

    # --- Новый функционал для членства группы ---
    def add_user_to_group(self, group: Group, user) -> Group:
        if user not in group.users:
            group.users.append(user)
            self.db.commit()
            self.db.refresh(group)
        return group

    def remove_user_from_group(self, group: Group, user) -> Group:
        if user in group.users:
            group.users.remove(user)
            self.db.commit()
            self.db.refresh(group)
        return group

    def get_group_members(self, group: Group):
        return group.users

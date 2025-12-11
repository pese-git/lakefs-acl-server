from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.policy_repository import PolicyRepository
from app.schemas.policy import PolicyCreate


class PolicyService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PolicyRepository(db)

    def create_policy(self, policy_data: PolicyCreate):
        if self.repo.get_by_name(policy_data.name):
            raise HTTPException(status_code=409, detail="Policy already exists")
        return self.repo.create(policy_data)

    def get_policy(self, policy_id: int):
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return policy

    def update_policy(self, policy_id: int, policy_data: PolicyCreate):
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return self.repo.update(policy, policy_data)

    def list_policies(self):
        return self.repo.list_all()

    def delete_policy(self, policy_id: int):
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        self.repo.delete(policy)
        return None

    def assign_policy_to_user(self, policy_id: int, user_id: int):
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository(self.db)
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repo.assign_policy_to_user(policy, user)

    def remove_policy_from_user(self, policy_id: int, user_id: int):
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository(self.db)
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repo.remove_policy_from_user(policy, user)

    def assign_policy_to_group(self, policy_id: int, group_id: int):
        from app.repositories.group_repository import GroupRepository
        group_repo = GroupRepository(self.db)
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        group = group_repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return self.repo.assign_policy_to_group(policy, group)

    def remove_policy_from_group(self, policy_id: int, group_id: int):
        from app.repositories.group_repository import GroupRepository
        group_repo = GroupRepository(self.db)
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        group = group_repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return self.repo.remove_policy_from_group(policy, group)

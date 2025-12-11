from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.policy_repository import PolicyRepository
from app.schemas.policy import PolicyCreate


class PolicyService:
    def __init__(self, db: Session):
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

    def list_policies(self):
        return self.repo.list_all()

    def delete_policy(self, policy_id: int):
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        self.repo.delete(policy)
        return None

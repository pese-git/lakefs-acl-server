from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.schemas.policy import PolicyCreate


class PolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Policy]:
        return self.db.query(Policy).filter(Policy.name == name).first()

    def get_by_id(self, policy_id: int) -> Optional[Policy]:
        return self.db.query(Policy).filter(Policy.id == policy_id).first()

    def create(self, policy_data: PolicyCreate) -> Policy:
        policy = Policy(name=policy_data.name, document=policy_data.document)
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def list_all(self) -> List[Policy]:
        return self.db.query(Policy).all()

    def delete(self, policy: Policy):
        self.db.delete(policy)
        self.db.commit()

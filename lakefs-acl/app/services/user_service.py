from fastapi import HTTPException, Response
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, user_data: UserCreate):
        if self.repo.get_by_username(user_data.username):
            raise HTTPException(status_code=409, detail="Username already registered")
        user = self.repo.create(user_data)
        return UserRead.model_validate(user)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def list_users(self):
        return self.repo.list_all()

    def delete_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.repo.delete(user)
        return Response(status_code=204, content="")

    def delete_user_by_username(self, username: str):
        user = self.repo.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.repo.delete(user)
        return Response(status_code=204, content="")

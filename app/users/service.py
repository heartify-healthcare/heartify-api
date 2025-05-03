from sqlalchemy.orm import Session
from typing import Optional, List
from app.users.repository import UserRepository
from app.users.entity import User
from app.users.schema import UserCreateSchema, UserUpdateSchema

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreateSchema) -> User:
        user = User(
            username=data.username,
            email=data.email,
            phonenumber=data.phonenumber,
            password=data.password  # NOTE: You should hash this in real apps!
        )
        return self.repo.create(user)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.repo.get_all()

    def update_user(self, user_id: int, data: UserUpdateSchema) -> Optional[User]:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        return self.repo.update(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.repo.get_by_id(user_id)
        if user:
            self.repo.delete(user)
            return True
        return False

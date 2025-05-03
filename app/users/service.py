from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any, Tuple
from app.users.repository import UserRepository
from app.users.entity import User
from app.users.schema import UserCreateSchema, UserUpdateSchema

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreateSchema) -> Tuple[Optional[User], Optional[Dict[str, str]]]:
        # Check if username already exists
        if self.repo.get_by_username(data.username):
            return None, {"error": "Username already exists"}
            
        # Check if email already exists
        if self.repo.get_by_email(data.email):
            return None, {"error": "Email already exists"}
            
        # Check if phonenumber already exists
        if data.phonenumber and self.repo.get_by_phonenumber(data.phonenumber):
            return None, {"error": "Phone number already exists"}
        
        user = User(
            username=data.username,
            email=data.email,
            phonenumber=data.phonenumber,
            password=data.password,  # NOTE: this one will be hashed using bcrypt later
            role=data.role
        )
        return self.repo.create(user), None

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.repo.get_all()

    def update_user(self, user_id: int, data: UserUpdateSchema) -> Tuple[Optional[User], Optional[Dict[str, str]]]:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None, {"error": "User not found"}
            
        update_data = data.dict(exclude_unset=True)
        
        # Check if username is being updated and already exists
        if "username" in update_data and update_data["username"] != user.username:
            if self.repo.get_by_username(update_data["username"]):
                return None, {"error": "Username already exists"}
                
        # Check if email is being updated and already exists
        if "email" in update_data and update_data["email"] != user.email:
            if self.repo.get_by_email(update_data["email"]):
                return None, {"error": "Email already exists"}
                
        # Check if phonenumber is being updated and already exists
        if "phonenumber" in update_data and update_data["phonenumber"] != user.phonenumber:
            if update_data["phonenumber"] and self.repo.get_by_phonenumber(update_data["phonenumber"]):
                return None, {"error": "Phone number already exists"}
        
        for key, value in update_data.items():
            setattr(user, key, value)
            
        return self.repo.update(user), None

    def delete_user(self, user_id: int) -> bool:
        user = self.repo.get_by_id(user_id)
        if user:
            self.repo.delete(user)
            return True
        return False
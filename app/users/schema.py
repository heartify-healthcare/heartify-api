from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserCreateSchema(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    phonenumber: Optional[str] = None
    password: constr(min_length=6)
    role: Optional[str] = "user"  # role field with default value

class UserUpdateSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    phonenumber: Optional[str]
    is_verified: Optional[bool]
    role: Optional[str]

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    phonenumber: Optional[str]
    is_verified: bool
    role: str

    class Config:
        orm_mode = True
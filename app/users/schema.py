from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserCreateSchema(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    phonenumber: Optional[str] = None
    password: constr(min_length=6)

class UserUpdateSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    phonenumber: Optional[str]
    is_verified: Optional[bool]

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    phonenumber: Optional[str]
    is_verified: bool

    class Config:
        orm_mode = True

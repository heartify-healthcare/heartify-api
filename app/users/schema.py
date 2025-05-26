from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional

class UserCreateSchema(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    phonenumber: Optional[str] = None
    password: constr(min_length=6)
    role: Optional[str] = "user"  # role field with default value

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['user', 'admin']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {allowed_roles}')
        return v

    @validator('phonenumber')
    def validate_phonenumber(cls, v):
        if v is not None and len(v.strip()) == 0:
            return None  # Convert empty strings to None
        return v

class UserUpdateSchema(BaseModel):
    username: Optional[constr(min_length=3)] = None
    email: Optional[EmailStr] = None
    phonenumber: Optional[str] = None
    password: Optional[constr(min_length=6)] = None  # Allow password updates
    is_verified: Optional[bool] = None
    role: Optional[str] = None

    @validator('role')
    def validate_role(cls, v):
        if v is not None:
            allowed_roles = ['user', 'admin']
            if v not in allowed_roles:
                raise ValueError(f'Role must be one of: {allowed_roles}')
        return v

    @validator('phonenumber')
    def validate_phonenumber(cls, v):
        if v is not None and len(v.strip()) == 0:
            return None  # Convert empty strings to None
        return v

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    phonenumber: Optional[str]
    is_verified: bool
    role: str

    class Config:
        orm_mode = True

class UserProfileSchema(BaseModel):
    """Schema for user profile updates (excludes sensitive fields)"""
    username: Optional[constr(min_length=3)] = None
    email: Optional[EmailStr] = None
    phonenumber: Optional[str] = None

    @validator('phonenumber')
    def validate_phonenumber(cls, v):
        if v is not None and len(v.strip()) == 0:
            return None  # Convert empty strings to None
        return v
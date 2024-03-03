from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional



class UserBase(BaseModel):
    username: str
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    pass

class UserInDb(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None


from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional
from api.schemas.user import UserResponse

class PostBase(BaseModel):
    author_id: int
    author: Optional[UserResponse]
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PostCreate(PostBase):
    replied_to_id: Optional[int]
    pass

class PostUpdate(BaseModel):
    content: str
class PostResponse(PostBase):
    id: int
    replied_to_id: Optional[int]
    # user: Optional[UserResponse]

class PostInDb(PostResponse):
    pass

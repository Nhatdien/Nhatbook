from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    author_id: int
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PostCreate(PostBase):
    replied_to_id: Optional[int]
    pass

class PostResponse(PostBase):
    id: int
    replied_to_id: Optional[int]
    replies: Optional[list[int]]

class PostInDb(PostResponse):
    pass

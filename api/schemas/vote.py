from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class VoteBase(BaseModel):
    vote_type: str
    user_id: int
    post_id: int


class VoteCreate(VoteBase):
    pass

class VoteResponse(VoteBase):
    id: int
    pass

class VoteInDb(VoteBase):
    pass

class VoteUpdate(VoteBase):
    pass

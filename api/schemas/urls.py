from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class UrlResponse(BaseModel):
    id: int
    long_url: str
    short_url: str
    created_at: datetime
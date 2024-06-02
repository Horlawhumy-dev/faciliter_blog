from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Forward declaration to handle circular import
from .post import Post

class AuthorBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    posts: List["Post"] = []

    class Config:
        from_attributes = True

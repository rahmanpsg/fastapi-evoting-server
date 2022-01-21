from pydantic import BaseModel
from typing import Optional

from schemas.user import User


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None


class Authentication(BaseModel):
    token: Token
    user: User

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    nama: str
    username: str


class UserCreate(UserBase):
    password: Optional[str]
    role: Optional[str] = 'pemilih'


class User(UserBase):
    id: int
    role: str
    password: str
    face_recognition: Optional[bool]

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    message: str
    item: Optional[User] = None

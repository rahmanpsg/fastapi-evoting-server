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
    status: bool

    class Config:
        orm_mode = True

# Pemilih output


class PemilihVoteCreate(BaseModel):
    id: int
    vote_nomor: Optional[int] = -1  # nomor default jika belum melakukan voting


class UserResponse(BaseModel):
    message: str
    item: Optional[User] = None

from pydantic import BaseModel


class User(BaseModel):
    nama: str
    username: str
    # password: str
    role: str
    status: bool

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    password: str

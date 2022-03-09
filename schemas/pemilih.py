from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class PemilihBase(BaseModel):
    nik: constr(min_length=16, max_length=16)
    nama: str
    username: str
    alamat: str
    telpon: Optional[str]


class PemilihCreate(PemilihBase):
    password: Optional[str]
    status: Optional[bool] = None
    face_recognition: Optional[bool]


class PemilihVerif(BaseModel):
    status: bool


class Pemilih(PemilihBase):
    id: int
    password: str
    status: Optional[bool]
    face_recognition: Optional[bool]

    class Config:
        orm_mode = True

# Pemilih output


class PemilihVoteCreate(BaseModel):
    id: str
    vote_nomor: Optional[str] = -1  # nomor default jika belum melakukan voting
    waktu: Optional[datetime] = None


class PemilihKotakSuara(PemilihVoteCreate):
    nama:str
    username:str


class PemilihResponse(BaseModel):
    message: str
    item: Optional[Pemilih] = None

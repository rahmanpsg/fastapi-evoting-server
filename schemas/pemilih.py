from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class PemilihBase(BaseModel):
    nik: constr(min_length=16, max_length=16)
    nama: str
    username: str
    alamat: str
    status: Optional[bool] = None


class PemilihCreate(PemilihBase):
    password: Optional[str]


class PemilihVerif(BaseModel):
    status: bool


class Pemilih(PemilihBase):
    id: int
    password: str

    class Config:
        orm_mode = True

# Pemilih output


class PemilihVoteCreate(BaseModel):
    id: str
    vote_nomor: Optional[str] = -1  # nomor default jika belum melakukan voting
    waktu: Optional[datetime] = None


class PemilihKotakSuara(PemilihBase, PemilihVoteCreate):
    pass


class PemilihResponse(BaseModel):
    message: str
    item: Optional[Pemilih] = None

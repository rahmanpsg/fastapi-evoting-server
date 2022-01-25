from typing import Optional
from fastapi import Form
from pydantic import BaseModel, HttpUrl


class KandidatBase(BaseModel):
    nama: str
    keterangan: str


class KandidatVoteCreate(BaseModel):
    id: int
    nomor: int


class KandidatCreate(KandidatBase):
    @classmethod
    def as_form(cls, nama: str = Form(...), keterangan: str = Form(...)) -> 'KandidatCreate':
        return cls(nama=nama, keterangan=keterangan)


class Kandidat(KandidatBase):
    id: int
    foto: Optional[str] = None

    class Config:
        orm_mode = True


class KandidatHitungCepat(Kandidat, KandidatVoteCreate):
    jumlah: int


class KandidatResponse(BaseModel):
    message: str
    item: Optional[Kandidat] = None

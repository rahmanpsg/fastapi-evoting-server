from typing import Optional
from fastapi import Form
from pydantic import BaseModel, HttpUrl


class KandidatBase(BaseModel):
    nama: str
    keterangan: str


class KandidatCreate(KandidatBase):
    @classmethod
    def as_form(cls, nama: str = Form(...), keterangan: str = Form(...)) -> 'KandidatCreate':
        return cls(nama=nama, keterangan=keterangan)


class Kandidat(KandidatBase):
    id: str
    nama: str
    foto: Optional[str] = None
    keterangan: str

    class Config:
        orm_mode = True


class KandidatResponse(BaseModel):
    message: str
    kandidat: Optional[Kandidat] = None

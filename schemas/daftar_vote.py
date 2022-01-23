from datetime import date, time
from typing import Optional
from pydantic import BaseModel

from schemas.kandidat import KandidatVoteCreate
from schemas.user import PemilihVoteCreate


class DaftarVoteBase(BaseModel):
    nama: str
    keterangan: str
    tanggal_mulai: date
    tanggal_selesai: date
    jam_mulai: time
    jam_selesai: time


class DaftarVoteCreate(DaftarVoteBase):
    status: Optional[bool] = True


class DaftarVoteList(BaseModel):
    list_kandidat: Optional[list[KandidatVoteCreate]]
    list_pemilih: Optional[list[PemilihVoteCreate]]


class DaftarVote(DaftarVoteBase):
    id: int
    list_kandidat: Optional[list[KandidatVoteCreate]]
    list_pemilih: Optional[list[PemilihVoteCreate]]
    status: bool

    class Config:
        orm_mode = True


class DaftarVoteResponse(BaseModel):
    message: str
    item: Optional[DaftarVote] = None

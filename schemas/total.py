from datetime import datetime
from pydantic import BaseModel


class Total(BaseModel):
    kandidat: int
    pemilih: int
    vote_aktif: int


class Perolehan(BaseModel):
    waktu: datetime
    total: int


class TotalKandidat(BaseModel):
    nama: str
    perolehan: list[Perolehan]


class TotalPerolehanSuara(BaseModel):
    telah_memilih: int
    belum_memilih: int
    kandidat: list[TotalKandidat]

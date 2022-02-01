from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from config.db import get_db
import repository.cetak as cetakRepository

cetakRoute = APIRouter(prefix='/cetak', tags=['Cetak'])


@cetakRoute.get('/kandidat', response_class=FileResponse)
async def cetak_kandidat(db: Session = Depends(get_db)):
    return cetakRepository.cetak_kandidat(db)


@cetakRoute.get('/pemilih', response_class=FileResponse)
async def cetak_pemilih(db: Session = Depends(get_db)):
    return cetakRepository.cetak_pemilih(db)


@cetakRoute.get('/daftarvote', response_class=FileResponse)
async def cetak_daftar_vote(db: Session = Depends(get_db)):
    return cetakRepository.cetak_daftar_vote(db)

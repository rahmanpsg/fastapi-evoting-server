from fastapi import APIRouter, BackgroundTasks,  Depends, status
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.pemilih import Pemilih, PemilihCreate, PemilihResponse, PemilihVerif

from services.oauth2 import get_current_user
from repository import pemilih as pemilihRepository


pemilihRoute = APIRouter(prefix="/pemilih", tags=['Pemilih'])


@pemilihRoute.get("/", response_model=list[Pemilih])
async def all(db: Session = Depends(get_db), current_user: Pemilih = Depends(get_current_user)):
    return pemilihRepository.get_all(db)


@pemilihRoute.post("/", response_model=PemilihResponse, status_code=status.HTTP_201_CREATED)
async def create(pemilih: PemilihCreate,bg_task: BackgroundTasks,  db: Session = Depends(get_db), current_user: Pemilih = Depends(get_current_user)):
    return await pemilihRepository.create(pemilih,bg_task, db)


@pemilihRoute.put('/{id}', response_model=PemilihResponse, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, pemilih: PemilihCreate,  db: Session = Depends(get_db), current_user: Pemilih = Depends(get_current_user)):
    return await pemilihRepository.update(id, pemilih, db)


@pemilihRoute.delete("/{id}", response_model=PemilihResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int,  db: Session = Depends(get_db),
                 current_user: Pemilih = Depends(get_current_user)):
    return await pemilihRepository.delete(id,  db)


@pemilihRoute.post("/verifikasi/{id}", response_model=PemilihResponse, status_code=status.HTTP_202_ACCEPTED)
async def verifikasi(id: int, pemilih: PemilihVerif,  db: Session = Depends(get_db), current_user: Pemilih = Depends(get_current_user)):
    return await pemilihRepository.verifikasi(id, pemilih, db)


@pemilihRoute.get("/{id}", response_model=Pemilih)
async def get_pemilih(id: int, db: Session = Depends(get_db), current_user: Pemilih = Depends(get_current_user)):
    return pemilihRepository.get_pemilih(id, db)

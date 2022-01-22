import asyncio
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, status
from sqlalchemy.orm import Session
from config.db import get_db

from schemas.kandidat import Kandidat, KandidatCreate, KandidatResponse
from schemas.user import User
from services.oauth2 import get_current_user
from repository import kandidat as kandidatRepository


kandidatRoute = APIRouter(prefix="/kandidat", tags=['Kandidat'])


@kandidatRoute.get("/", response_model=list[Kandidat])
async def all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    await asyncio.sleep(1)
    return kandidatRepository.get_all(db)


@kandidatRoute.get("/foto/{id}")
def foto(id: int, db: Session = Depends(get_db)):
    return kandidatRepository.get_foto(id, db)


@kandidatRoute.post("/", response_model=KandidatResponse, status_code=status.HTTP_201_CREATED)
async def create(kandidat: KandidatCreate = Depends(KandidatCreate.as_form), file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # await asyncio.sleep(3)
    return await kandidatRepository.create(kandidat, db, file)


@kandidatRoute.put('/{id}', response_model=KandidatResponse, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, kandidat: KandidatCreate = Depends(KandidatCreate.as_form), file: Optional[UploadFile] = File(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # await asyncio.sleep(3)
    return await kandidatRepository.update(id, kandidat, db, file)


@kandidatRoute.delete("/{id}", response_model=KandidatResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int, bg_task: BackgroundTasks, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    await asyncio.sleep(1)
    return await kandidatRepository.delete(id, bg_task, db)

import asyncio
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.daftar_vote import DaftarVote, DaftarVoteCreate, DaftarVoteList, DaftarVoteResponse
from schemas.kandidat import KandidatVoteCreate
from services.oauth2 import get_current_user
from repository import daftar_vote as daftarVoteRepository

daftarVoteRoute = APIRouter(prefix="/daftarVote", tags=['Daftar Vote'])


@daftarVoteRoute.get("/", response_model=list[DaftarVote])
async def all(db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    return daftarVoteRepository.get_all(db)


@daftarVoteRoute.post("/", response_model=DaftarVoteResponse, status_code=status.HTTP_201_CREATED)
async def create(daftarVote: DaftarVoteCreate, db: Session = Depends(get_db)):
    return daftarVoteRepository.create(daftarVote, db)


@daftarVoteRoute.put('/{id}', response_model=DaftarVoteResponse, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, daftarVote: DaftarVoteCreate,  db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return await daftarVoteRepository.update(id, daftarVote, db)


@daftarVoteRoute.delete("/{id}", response_model=DaftarVoteResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int,  db: Session = Depends(get_db),
                 current_user: DaftarVote = Depends(get_current_user)):
    return await daftarVoteRepository.delete(id,  db)


@daftarVoteRoute.get("/list/{id}", response_model=DaftarVoteList)
def get_list_kandidat_and_pemilih(id: int, db: Session = Depends(get_db)):
    return daftarVoteRepository.get_list(id, db)


@daftarVoteRoute.post("list/kandidat/{id}")
def add_list_kandidat(id: int, kandidat: KandidatVoteCreate, db: Session = Depends(get_db)):
    return daftarVoteRepository.add_kandidat(id, kandidat, db)

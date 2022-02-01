import asyncio
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.daftar_vote import DaftarVote, DaftarVoteResponse
from services.oauth2 import get_current_user
from repository import vote as voteRepository

voteRoute = APIRouter(prefix="/vote", tags=['Vote'])


@voteRoute.get("/{id_user}", response_model=list[DaftarVote])
async def all(db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return voteRepository.get_all(db)


@voteRoute.post("/{id_daftarVote}/{id_pemilih}", response_model=DaftarVoteResponse, status_code=status.HTTP_201_CREATED)
async def add_voting(id_daftarVote: int, id_pemilih: int, vote_nomor: int, db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return voteRepository.add_voting(id_daftarVote, id_pemilih, vote_nomor, db)

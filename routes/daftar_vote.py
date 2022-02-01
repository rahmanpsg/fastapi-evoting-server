from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.daftar_vote import DaftarVote, DaftarVoteCreate, DaftarVoteList, DaftarVotePemilih, DaftarVoteResponse
from schemas.kandidat import KandidatHitungCepat, KandidatVoteCreate
from schemas.pemilih import PemilihKotakSuara, PemilihVoteCreate
from services.oauth2 import get_current_user
from repository import daftar_vote as daftarVoteRepository

daftarVoteRoute = APIRouter(prefix="/daftarVote", tags=['Daftar Vote'])


@daftarVoteRoute.get("/", response_model=list[DaftarVote])
async def all(db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    # await asyncio.sleep(2)
    return daftarVoteRepository.get_all(db)


@daftarVoteRoute.post("/", response_model=DaftarVoteResponse, status_code=status.HTTP_201_CREATED)
async def create(daftarVote: DaftarVoteCreate, db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.create(daftarVote, db)


@daftarVoteRoute.put('/{id}', response_model=DaftarVoteResponse, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, daftarVote: DaftarVoteCreate,  db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return await daftarVoteRepository.update(id, daftarVote, db)


@daftarVoteRoute.delete("/{id}", response_model=DaftarVoteResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int,  db: Session = Depends(get_db),
                 current_user: DaftarVote = Depends(get_current_user)):
    return await daftarVoteRepository.delete(id,  db)


@daftarVoteRoute.get("/list/{id}", response_model=DaftarVoteList)
def get_list_kandidat_and_pemilih(id: int, db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.get_list(id, db)


@daftarVoteRoute.get("/kotaksuara/{id}", response_model=list[PemilihKotakSuara])
async def get_kotak_suara(id: int,  db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.get_kotak_suara(id, db)


@daftarVoteRoute.get("/hitungcepat/{id}", response_model=list[KandidatHitungCepat])
async def get_hitung_cepat(id: int,  db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.get_hitung_cepat(id, db)


@daftarVoteRoute.post("/list/kandidat/{id}", response_model=DaftarVoteResponse, status_code=status.HTTP_202_ACCEPTED)
async def add_list_kandidat(id: int, kandidats: list[KandidatVoteCreate], db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.add_list_kandidat(id, kandidats, db)


@daftarVoteRoute.post("/list/pemilih/{id}", response_model=DaftarVoteResponse, status_code=status.HTTP_202_ACCEPTED)
async def add_list_pemilih(id: int, pemilihs: list[PemilihVoteCreate], db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.add_list_pemilih(id, pemilihs, db)


@daftarVoteRoute.get("/pemilih/{id_pemilih}", response_model=list[DaftarVotePemilih], response_model_exclude=['list_pemilih'])
async def get_daftar_vote_pemilih(id_pemilih: int,  db: Session = Depends(get_db), current_user: DaftarVote = Depends(get_current_user)):
    return daftarVoteRepository.get_daftar_vote_pemilih(id_pemilih,  db)

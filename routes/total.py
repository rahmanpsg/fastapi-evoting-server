from fastapi import APIRouter, Depends,  status
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.total import Total, TotalPerolehanSuara
import repository.total as totalRepository
from services.oauth2 import get_current_user

totalRoute = APIRouter(prefix='/total', tags=['Total Data'])


@totalRoute.get('/', response_model=Total)
async def get_total_data(db: Session = Depends(get_db), current_user: Total = Depends(get_current_user)):
    return totalRepository.get_total_data(db)


@totalRoute.get("/perolehansuara/{id_daftarVote}/", response_model=TotalPerolehanSuara)
async def get_perolehan_suara(id_daftarVote: int,  db: Session = Depends(get_db), current_user: Total = Depends(get_current_user)):
    return totalRepository.get_perolehan_suara(id_daftarVote,  db)

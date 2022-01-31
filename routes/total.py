import asyncio
from fastapi import APIRouter, Depends,  status
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.total import Total, TotalPerolehanSuara
import repository.total as totalRepository

totalRoute = APIRouter(prefix='/total', tags=['Total Data'])


@totalRoute.get('/', response_model=Total)
async def get_total_data(db: Session = Depends(get_db)):
    # await asyncio.sleep(2)
    return totalRepository.get_total_data(db)


@totalRoute.get("/perolehansuara/{id_daftarVote}/", response_model=TotalPerolehanSuara)
async def get_perolehan_suara(id_daftarVote: int,  db: Session = Depends(get_db)):
    # await asyncio.sleep(2)
    return totalRepository.get_perolehan_suara(id_daftarVote,  db)

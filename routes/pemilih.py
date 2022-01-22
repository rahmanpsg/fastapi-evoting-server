from fastapi import APIRouter,  Depends, status
from sqlalchemy.orm import Session
from config.db import get_db

from schemas.user import User, UserCreate, UserResponse
from services.oauth2 import get_current_user
from repository import pemilih as pemilihRepository


pemilihRoute = APIRouter(prefix="/pemilih", tags=['Pemilih'])


@pemilihRoute.get("/", response_model=list[User])
async def all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return pemilihRepository.get_all(db)


@pemilihRoute.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(pemilih: UserCreate,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await pemilihRepository.create(pemilih, db)


@pemilihRoute.put('/{id}', response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, pemilih: UserCreate,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await pemilihRepository.update(id, pemilih, db)


@pemilihRoute.delete("/{id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int,  db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return await pemilihRepository.delete(id,  db)

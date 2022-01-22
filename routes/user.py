from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.user import User, UserCreate, UserResponse
from services.oauth2 import get_current_user
from repository import user as userRepository

userRoute = APIRouter(prefix="/user", tags=['User'])


@userRoute.get("/", response_model=list[User])
def all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return userRepository.get_all(db)


@userRoute.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return userRepository.create(user, db)


@userRoute.put('/{id}', response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, pemilih: UserCreate,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await userRepository.update(id, pemilih, db)


@userRoute.delete("/{id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int,  db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return await userRepository.delete(id,  db)

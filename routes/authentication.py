from ast import And
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db
from models.pemilih import Pemilihs
from models.user import Users
from schemas.authentication import Authentication, Token
from services.token import create_access_token

authRoute = APIRouter(prefix="/login", tags=['Authentication'])


@authRoute.post("/", response_model=Authentication)
async def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == req.username).first()

    if not user:
        user = db.query(Pemilihs).filter(
            Pemilihs.username == req.username).first()
        user.role = 'pemilih'

    if user and user.password == req.password:
        access_token = create_access_token(data={"sub": user.username})
        token = Token(access_token=access_token, token_type='bearer')
        return Authentication(token=token, user=user)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Username atau password salah")

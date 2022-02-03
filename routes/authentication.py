from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config.db import get_db
from models.pemilih import Pemilihs
from models.user import Users
from repository.pemilih import cek_username
from schemas.authentication import Authentication, Token
from schemas.pemilih import PemilihCreate, PemilihResponse
from services.error_handling import add_or_edit_exception
from services.token import create_access_token

authRoute = APIRouter(prefix="/login", tags=['Authentication'])


@authRoute.post("/", response_model=Authentication)
async def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == req.username).first()

    if not user:
        user = db.query(Pemilihs).filter(
            Pemilihs.username == req.username).first()
        if user:
            if user.status is not True:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Akun anda belum diaktifkan")

            user.role = 'pemilih'

    if user and user.password == req.password:
        access_token = create_access_token(data={"sub": user.username})
        token = Token(access_token=access_token, token_type='bearer')
        return Authentication(token=token, user=user)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Username atau password salah")


@authRoute.post("/registrasi", response_model=PemilihResponse, status_code=status.HTTP_201_CREATED)
async def registrasi(req: PemilihCreate,  db: Session = Depends(get_db)):
    try:
        cek_username(req.username, db)

        new = Pemilihs(
            nik=req.nik, nama=req.nama, username=req.username, password=req.password, alamat=req.alamat, status=None)
        db.add(new)
        db.commit()
        db.refresh(new)

        return PemilihResponse(message="Registrasi berhasil, akun anda akan dikonfirmasi oleh admin agar dapat digunakan", item=new)

    except SQLAlchemyError as e:
        add_or_edit_exception(e)

from email import message
import os
import uuid
import aiofiles
import aiofiles.os
from fastapi import BackgroundTasks, File, UploadFile, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import Users
from schemas.user import UserCreate, UserResponse
from services.error_handling import add_or_edit_exception

save_path = 'assets/foto/kandidat/'


def get_all(db: Session):
    return db.query(Users).filter(Users.role == 'pemilih').all()


async def create(req: UserCreate, db: Session):
    try:
        new = Users(
            nama=req.nama, username=req.username, password=req.password, role="pemilih")
        db.add(new)
        db.commit()
        db.refresh(new)

        return UserResponse(message="Pemilih berhasil ditambahkan", item=new)

    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def update(id: int, req: UserCreate, db: Session):
    try:
        pemilih = cek_pemilih(id, db)
        pemilih.update(req.dict())
        db.commit()

        return UserResponse(message="Pemilih berhasil diubah")
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def delete(id: int,  db: Session):
    try:
        pemilih = cek_pemilih(id, db)

        pemilih.delete(synchronize_session=False)
        db.commit()

        return UserResponse(message="Pemilih berhasil dihapus")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def cek_pemilih(id: int, db: Session):
    pemilih = db.query(Users).filter(
        Users.id == id and Users.role == 'pemilih')

    if not pemilih.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID Pemilih tidak ditemukan")

    return pemilih

from email import message
import os
import uuid
import aiofiles
import aiofiles.os
from fastapi import BackgroundTasks, File, UploadFile, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.kandidat import Kandidats
from schemas.kandidat import KandidatCreate, KandidatResponse

save_path = 'assets/foto/kandidat/'


def get_all(db: Session):
    return db.query(Kandidats).all()


def get_kandidat(id: int, db: Session):
    kandidat = db.query(Kandidats).get(id)

    return kandidat


def get_foto(id: int, db: Session):
    kandidat = cek_kandidat(id, db).first()

    return FileResponse(save_path + kandidat.foto)


async def create(req: KandidatCreate, db: Session, file: UploadFile = File(...)):
    try:
        if file.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Hanya file foto yang dapat diupload")

        file_name = f'{uuid.uuid4().hex}.jpg'

        out_file_path = os.path.join(save_path, file_name)

        new_kandidat = Kandidats(
            nama=req.nama, foto=file_name, keterangan=req.keterangan)
        db.add(new_kandidat)
        db.commit()
        db.refresh(new_kandidat)

        async with aiofiles.open(out_file_path, 'wb') as output:
            foto = await file.read()
            await output.write(foto)

        return KandidatResponse(message="Kandidat berhasil ditambahkan", item=new_kandidat)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


async def update(id: int, req: KandidatCreate, db: Session, file: UploadFile = File(None)):
    kandidat = cek_kandidat(id, db)
    kandidat.update(req.dict())
    db.commit()

    if file:
        out_file_path = os.path.join(save_path, kandidat.first().foto)

        async with aiofiles.open(out_file_path, 'wb') as output:
            foto = await file.read()
            await output.write(foto)

    return KandidatResponse(message="Kandidat berhasil diubah")


async def delete(id: int, bg_task: BackgroundTasks, db: Session):
    try:
        kandidat = cek_kandidat(id, db)

        file_name = kandidat.first().foto

        kandidat.delete(synchronize_session=False)
        db.commit()

        bg_task.add_task(hapus_file, save_path + file_name)

        return KandidatResponse(message="Kandidat berhasil dihapus")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


async def hapus_file(path: str):
    await aiofiles.os.remove(path)
    print(path + " dihapus...")


def cek_kandidat(id: int, db: Session):
    kandidat = db.query(Kandidats).filter(Kandidats.id == id)

    if not kandidat.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID Kandidat tidak ditemukan")

    return kandidat

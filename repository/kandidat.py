import uuid
from fastapi import BackgroundTasks, File, UploadFile, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.kandidat import Kandidats
from schemas.kandidat import KandidatCreate, KandidatResponse
import cloudinary
import cloudinary.uploader
import cloudinary.api


def get_all(db: Session):
    return db.query(Kandidats).all()


def get_kandidat(id: int, db: Session):
    kandidat = db.query(Kandidats).get(id)
    return kandidat


async def create(req: KandidatCreate, db: Session, file: UploadFile):
    try:
        if file.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Hanya file foto yang dapat diupload")

        file_name = f'{uuid.uuid4().hex}'

        foto = await file.read()
        upload = cloudinary.uploader.upload(
            foto, public_id=file_name, folder="kandidat", invalidate=True)

        print(upload['url'])

        url = upload['url'].split('upload/')[1]

        new_kandidat = Kandidats(
            nama=req.nama, foto=url, keterangan=req.keterangan)
        db.add(new_kandidat)
        db.commit()
        db.refresh(new_kandidat)

        return KandidatResponse(message="Kandidat berhasil ditambahkan", item=new_kandidat)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


async def update(id: int, req: KandidatCreate, db: Session, file: UploadFile = File(None)):
    kandidat = cek_kandidat(id, db)

    if file:
        foto = await file.read()
        url = kandidat.first().foto
        public_id = url.split('/')[-1].replace('.jpg', '')

        upload = cloudinary.uploader.upload(
            foto, public_id=public_id, folder="kandidat", invalidate=True)

        url = upload['url'].split('upload/')[-1]
        kandidat.update({'foto': url})

    kandidat.update(req.dict())
    db.commit()

    return KandidatResponse(message="Kandidat berhasil diubah", item=kandidat.first())


async def delete(id: int, bg_task: BackgroundTasks, db: Session):
    try:
        kandidat = cek_kandidat(id, db)

        file_name = kandidat.first().foto

        kandidat.delete(synchronize_session=False)
        db.commit()

        bg_task.add_task(hapus_file, file_name)

        return KandidatResponse(message="Kandidat berhasil dihapus")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def hapus_file(public_id: str):
    cloudinary.uploader.destroy("kandidat/"+public_id)
    print(public_id + " dihapus...")


def cek_kandidat(id: int, db: Session):
    kandidat = db.query(Kandidats).filter(Kandidats.id == id)

    if not kandidat.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID Kandidat tidak ditemukan")

    return kandidat

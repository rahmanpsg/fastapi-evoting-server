from fastapi import BackgroundTasks, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.pemilih import Pemilihs
from models.user import Users
from schemas.pemilih import PemilihCreate, PemilihResponse, PemilihVerif
from services.error_handling import add_or_edit_exception
from services.sms_gateway import kirim_sms
import cloudinary
import os

save_path = 'assets/foto/kandidat/'


def get_all(db: Session):
    return db.query(Pemilihs).all()


def get_pemilih(id: int, db: Session):
    try:
        pemilih = cek_pemilih(id, db).first()

        return pemilih
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def create(req: PemilihCreate,bg_task: BackgroundTasks, db: Session):
    try:
        cek_username(req.username, db)

        new = Pemilihs(
            nik=req.nik, nama=req.nama, username=req.username, password=req.password, alamat=req.alamat, status=req.status, telpon=req.telpon)
        db.add(new)
        db.commit()
        db.refresh(new)

        pesan = f"Akun anda telah didaftarkan untuk melakukan online voting. Silahkan login menggunakan username : {req.username}, password : {req.password} di {os.getenv('CLIENT_URL')}."

        bg_task.add_task(kirim_sms, req.telpon, pesan)

        return PemilihResponse(message="Pemilih berhasil ditambahkan", item=new)

    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def update(id: int, req: PemilihCreate, db: Session):
    try:
        pemilih = cek_pemilih(id, db)

        cek_username(req.username, db)

        pemilih.update(req.dict())
        db.commit()

        return PemilihResponse(message="Pemilih berhasil diubah")
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def delete(id: int, bg_task: BackgroundTasks,  db: Session):
    try:
        pemilih = cek_pemilih(id, db)

        pemilih.delete(synchronize_session=False)
        db.commit()

        bg_task.add_task(hapus_file, id)

        return PemilihResponse(message="Pemilih berhasil dihapus")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


async def verifikasi(id: int, req: PemilihVerif, db: Session):
    try:
        pemilih = db.query(Pemilihs).get(id)

        if not pemilih:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Pemilih tidak ditemukan")

        pemilih.status = req.status

        db.commit()

        return PemilihResponse(message="Pemilih berhasil di{}".format("terima" if req.status else "tolak"))
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


def cek_pemilih(id: int, db: Session):
    pemilih = db.query(Pemilihs).filter(
        Pemilihs.id == id)

    if not pemilih.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID Pemilih tidak ditemukan")

    return pemilih

def hapus_file(id: str):
    public_ids = []

    for i in range(1,101):
        public_ids.append('training/{}.{}'.format(id, i))

    delete = cloudinary.api.delete_resources(public_ids)


def cek_username(username: str, db: Session):
    cek = db.query(Users.id).filter(Users.username == username).count()

    if cek > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username telah digunakan")

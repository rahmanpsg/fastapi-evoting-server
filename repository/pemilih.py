from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.pemilih import Pemilihs
from models.user import Users
from schemas.pemilih import PemilihCreate, PemilihResponse, PemilihVerif
from services.error_handling import add_or_edit_exception

save_path = 'assets/foto/kandidat/'


def get_all(db: Session):
    return db.query(Pemilihs).all()


def get_pemilih(id: int, db: Session):
    try:
        pemilih = cek_pemilih(id, db).first()

        return pemilih
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def create(req: PemilihCreate, db: Session):
    try:
        cek_username(req.username, db)

        new = Pemilihs(
            nik=req.nik, nama=req.nama, username=req.username, password=req.password, alamat=req.alamat, status=req.status)
        db.add(new)
        db.commit()
        db.refresh(new)

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


async def delete(id: int,  db: Session):
    try:
        pemilih = cek_pemilih(id, db)

        pemilih.delete(synchronize_session=False)
        db.commit()

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


def cek_username(username: str, db: Session):
    cek = db.query(Users.id).filter(Users.username == username).count()

    if cek > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username telah digunakan")

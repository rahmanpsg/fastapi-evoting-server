import json
from xmlrpc.client import DateTime
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.daftar_vote import DaftarVotes
from schemas.daftar_vote import DaftarVote, DaftarVoteCreate, DaftarVoteResponse
from schemas.kandidat import KandidatVoteCreate
from services.error_handling import add_or_edit_exception


def get_all(db: Session):
    return db.query(DaftarVotes).all()


def create(req: DaftarVoteCreate, db: Session):
    try:
        # v = validate(instance=req.list_kandidat, schema=Kandidat)
        # list = req.dict(include={'list_kandidat', 'list_pemilih'})

        # print(list['list_kandidat'])
        new = DaftarVotes(
            nama=req.nama,
            keterangan=req.keterangan,
            tanggal_mulai=req.tanggal_mulai,
            tanggal_selesai=req.tanggal_selesai,
            jam_mulai=req.jam_mulai,
            jam_selesai=req.jam_selesai,
            # list_kandidat=list['list_kandidat'],
            # list_pemilih=list['list_pemilih']
            # status=True,
            # created_at='',
            # updated_at=''
        )
        db.add(new)
        db.commit()
        db.refresh(new)

        return DaftarVoteResponse(message="Daftar Vote berhasil ditambahkan", item=new)

    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def update(id: int, req: DaftarVoteCreate, db: Session):
    try:
        user = cek_daftar_vote(id, db)
        user.update(req.dict())
        db.commit()

        return DaftarVoteResponse(message="Daftar Vote berhasil diubah")
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def delete(id: int,  db: Session):
    try:
        user = cek_daftar_vote(id, db)

        user.delete(synchronize_session=False)
        db.commit()

        return DaftarVoteResponse(message="Daftar Vote berhasil dihapus")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def get_list(id: int, db: Session):
    list = db.query(DaftarVotes.list_kandidat, DaftarVotes.list_pemilih).filter(
        DaftarVotes.id == id).first()

    if not list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID Daftar Vote tidak ditemukan")
    return list


def add_kandidat(id: int, kandidat: KandidatVoteCreate, db: Session):
    daftar_vote = db.query(DaftarVotes).get(id)

    list_kandidat = daftar_vote.list_kandidat.copy()

    # cek jika nomor urut telah ada
    cek = next((i for i, d in enumerate(
        list_kandidat) if d['nomor'] == kandidat.nomor), None)

    if cek is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Nomor urut kandidat telah digunakan')

    list_kandidat.append(kandidat.dict())

    daftar_vote.list_kandidat = list_kandidat

    db.commit()

    return DaftarVoteResponse(message="Kandidat berhasil ditambahkan")


def solve(key, val, lis):
    return next((i for i, d in enumerate(lis) if d[key] == val), None)


def cek_daftar_vote(id: int, db: Session):
    daftar_vote = db.query(DaftarVotes).filter(
        DaftarVotes.id == id)

    if not daftar_vote.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID Daftar Vote tidak ditemukan")

    return daftar_vote

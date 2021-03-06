from datetime import datetime
import json
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.daftar_vote import DaftarVotes
from models.kandidat import Kandidats
from models.pemilih import Pemilihs
from models.user import Users
from schemas.daftar_vote import DaftarVoteCreate, DaftarVotePemilih, DaftarVoteResponse
from schemas.kandidat import KandidatHitungCepat, KandidatVoteCreate
from schemas.pemilih import PemilihKotakSuara, PemilihVoteCreate
from services.error_handling import add_or_edit_exception


def get_all(db: Session):
    return db.query(DaftarVotes).all()


def create(req: DaftarVoteCreate, db: Session):
    try:
        new = DaftarVotes(
            nama=req.nama,
            keterangan=req.keterangan,
            tanggal_mulai=req.tanggal_mulai,
            tanggal_selesai=req.tanggal_selesai,
            jam_mulai=req.jam_mulai,
            jam_selesai=req.jam_selesai,
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


def get_kotak_suara(id: int, db: Session):
    try:
        list = db.query(DaftarVotes.list_pemilih).filter(
            DaftarVotes.id == id).first()

        if not list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Daftar Vote tidak ditemukan")

        filter = sorted([pemilih for pemilih in list.list_pemilih if pemilih['waktu']],
                        key=lambda v: v['id'],)

        ids = (int(pemilih['id']) for pemilih in filter)
        
        pemilih = db.query(Pemilihs.nama, Pemilihs.username).filter(
            Pemilihs.id.in_(ids)).all()

        data: list[PemilihKotakSuara] = []

        if pemilih:
            for i in range(len(filter)):
                fil = filter[i]
                pem = pemilih[i]
                data.append(PemilihKotakSuara(id=fil['id'], vote_nomor=fil['vote_nomor'],
                            waktu=fil['waktu'], nama=pem['nama'], username=pem['username']))

        return data
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def get_hitung_cepat(id: int, db: Session):
    try:
        list = db.query(DaftarVotes.list_kandidat, DaftarVotes.list_pemilih).filter(
            DaftarVotes.id == id).first()

        if not list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Daftar Vote tidak ditemukan")

        ids = (kandidat['id'] for kandidat in list.list_kandidat)

        kandidat = db.query(Kandidats).filter(Kandidats.id.in_(ids)).all()

        # menghitung total vote
        vote = {}
        for pemilih in list.list_pemilih:
            if pemilih['vote_nomor'] in vote:
                vote[(pemilih['vote_nomor'])] += 1
            else:
                vote[pemilih['vote_nomor']] = 1

        data: list[KandidatHitungCepat] = []

        for i, list_kandidat in enumerate(list.list_kandidat):
            data.append(KandidatHitungCepat(id=list_kandidat['id'], nama=kandidat[i].nama, nomor=list_kandidat['nomor'],
                        keterangan=kandidat[i].keterangan, foto=kandidat[i].foto, jumlah=vote[str(
                            list_kandidat['nomor'])]
                if str(list_kandidat['nomor']) in vote else 0))

        return data

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def add_list_kandidat(id: int, kandidats: list[KandidatVoteCreate], db: Session):
    try:
        daftar_vote = db.query(DaftarVotes).get(id)

        if not daftar_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Daftar Vote tidak ditemukan")

        daftar_vote.list_kandidat = jsonable_encoder(kandidats)

        db.commit()

        return DaftarVoteResponse(message="Daftar Kandidat berhasil disimpan")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def add_list_pemilih(id: int, pemilihs: list[PemilihVoteCreate], db: Session):
    try:
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST, detail='Daftar Vote Aktif/Berjalan tidak dapat diubah')

        daftar_vote = db.query(DaftarVotes).get(id)

        if not daftar_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Daftar Vote tidak ditemukan")

        daftar_vote.list_pemilih = jsonable_encoder(pemilihs)

        db.commit()

        return DaftarVoteResponse(message="Daftar Pemilih berhasil disimpan")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


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


def get_daftar_vote_pemilih(id_pemilih: int, db: Session):
    query = db.execute(
        "SELECT *, JSON_UNQUOTE(JSON_EXTRACT(list_pemilih, REPLACE(JSON_UNQUOTE(JSON_SEARCH(list_pemilih, 'one', ':id', NULL, '$[*].id')), 'id', 'vote_nomor'))) as vote_nomor FROM daftar_vote WHERE JSON_SEARCH(list_pemilih, 'one', :id, NULL, '$[*].id') IS NOT NULL", {'id': id_pemilih}).all()

    daftar_vote: list[DaftarVotePemilih] = []

    for daftar in query:
        waktu_mulai = datetime.strptime(
            f"{daftar.tanggal_mulai} {daftar.jam_mulai}", "%Y-%m-%d %H:%M:%S")
        waktu_selesai = datetime.strptime(
            f"{daftar.tanggal_selesai} {daftar.jam_selesai}", "%Y-%m-%d %H:%M:%S")

        list_kandidat = [KandidatVoteCreate(
            id=int(kandidat['id']), nomor=int(kandidat['nomor'])) for kandidat in json.loads(daftar.list_kandidat)]

        telah_memilih = daftar.vote_nomor != '-1'

        daftar_vote.append(DaftarVotePemilih(id=daftar.id, nama=daftar.nama, keterangan=daftar.keterangan, tanggal_mulai=waktu_mulai.date(), jam_mulai=waktu_mulai.time(),
                                             tanggal_selesai=waktu_selesai.date(), jam_selesai=waktu_selesai.time(), list_kandidat=list_kandidat, telah_memilih=telah_memilih, vote_nomor=daftar.vote_nomor))

    return daftar_vote

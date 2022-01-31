from datetime import datetime
import random
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.daftar_vote import DaftarVotes

from models.kandidat import Kandidats
from models.pemilih import Pemilihs
from models.user import Users
from schemas.total import Perolehan, Total, TotalKandidat, TotalPerolehanSuara

import pandas as pd
import numpy as np


def get_total_data(db: Session):
    try:
        total_kandidat = db.query(Kandidats.id).count()
        total_pemilih = db.query(Pemilihs.id).filter(
            Pemilihs.status == True).count()

        now = datetime.now()

        total_vote_aktif = db.query(DaftarVotes.tanggal_mulai, DaftarVotes.jam_mulai).filter(
            func.timestamp(DaftarVotes.tanggal_mulai, DaftarVotes.jam_mulai) <= now, func.timestamp(DaftarVotes.tanggal_selesai, DaftarVotes.jam_selesai) >= now).count()

        return Total(kandidat=total_kandidat, pemilih=total_pemilih, vote_aktif=total_vote_aktif)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def get_perolehan_suara(id_daftarVote: int, db: Session):
    try:
        list = db.query(DaftarVotes).get(id_daftarVote)

        if not list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Daftar Vote tidak ditemukan")

        ids = (kandidat['id'] for kandidat in list.list_kandidat)

        kandidat_db = db.query(Kandidats.id, Kandidats.nama).filter(
            Kandidats.id.in_(ids)).all()

        telah_memilih = len([
            pemilih for pemilih in list.list_pemilih if pemilih['waktu']])
        belum_memilih = len(list.list_pemilih) - telah_memilih

        list_pemilih = sorted(list.list_pemilih,
                              key=lambda v: (v['waktu'] is not None, v['waktu']))

        list_pemilih_map = {pemilih['waktu']: int(pemilih['vote_nomor'])
                            for pemilih in list_pemilih if pemilih['waktu']}

        list_waktu: list[datetime] = [datetime.fromisoformat(
            s['waktu']) for s in list_pemilih if s['waktu']]

        waktu_mulai = datetime.combine(
            list.tanggal_mulai, list.jam_mulai)

        # waktu_selesai = datetime.fromisoformat(
        #     list_pemilih[-1]['waktu'] if list_pemilih[-1]['waktu'] else datetime.now().isoformat())
        waktu_selesai = datetime.combine(
            list.tanggal_selesai, list.jam_selesai)

        waktu_selesai = waktu_selesai if waktu_selesai < datetime.now(
        ) else datetime.now().replace(microsecond=0)

        # membuat daftar list waktu
        for i in range(11):
            waktu = random_date(start=waktu_mulai,
                                end=waktu_selesai, position=i / 10)
            list_waktu.append(waktu.to_pydatetime())

        list_waktu = sorted(list_waktu, key=lambda v: v)

        kandidats: list[TotalKandidat] = []

        # membuat daftar list kandidat
        for list_kandidat in list.list_kandidat:
            perolehans: list[Perolehan] = []
            total = 0
            for waktu in list_waktu:
                if str(waktu) in list_pemilih_map and list_pemilih_map[str(waktu)] == list_kandidat['nomor']:
                    total += 1
                perolehans.append(Perolehan(waktu=waktu, total=total))

            nama = next(
                (kandidat['nama'] for kandidat in kandidat_db if kandidat['id'] == list_kandidat['id']), None)

            kandidat = TotalKandidat(
                nama=nama, perolehan=perolehans)

            kandidats.append(kandidat)

        return TotalPerolehanSuara(telah_memilih=telah_memilih, belum_memilih=belum_memilih, kandidat=kandidats)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def random_date(start, end, position=None):
    start, end = pd.Timestamp(
        start.strftime("%m/%d/%y %I:%M%p")), pd.Timestamp(end.strftime("%m/%d/%y %I:%M%p"))
    delta = (end - start).total_seconds()
    if position is None:
        offset = np.random.uniform(0., delta)
    else:
        offset = position * delta
    offset = pd.offsets.Second(offset)
    t = start + offset
    return t

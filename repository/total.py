from datetime import datetime
import random
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.daftar_vote import DaftarVotes

from models.kandidat import Kandidats
from models.user import Users
from schemas.total import Perolehan, Total

import pandas as pd
import numpy as np


def get_total_data(db: Session):
    try:
        total_kandidat = db.query(Kandidats.id).count()
        total_pemilih = db.query(Users.id).filter(
            Users.role == 'pemilih').count()

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

        # filter = sorted([pemilih for pemilih in list.list_pemilih if pemilih['waktu']],
        #                 key=lambda v: v['id'],)

        # ids = (pemilih['id'] for pemilih in list.list_pemilih)

        # pemilih = db.query(Users.nama, Users.username).filter(
        #     Users.id.in_(ids)).all()

        telah_memilih = len([
            pemilih for pemilih in list.list_pemilih if pemilih['waktu']])
        belum_memilih = len(list.list_pemilih) - telah_memilih

        print(list.list_pemilih)

        waktu_mulai = datetime.combine(
            list.tanggal_mulai, list.jam_mulai)

        # perolehan = Perolehan(waktu=waktu_mulai, total=0)

        sort = sorted(list.list_pemilih,
                      key=lambda v: (v['waktu'] is not None, v['waktu']))

        td_waktu = datetime.fromisoformat(sort[2]['waktu']) - waktu_mulai

        td = datetime.fromisoformat(
            sort[2]['waktu']) - datetime.fromisoformat(sort[1]['waktu'])

        # days, hours, minutes = td.days, td.seconds // 3600, td.seconds % 3600 / 60.0
        # print(waktu_mulai)

        # print(random_date(start=waktu_mulai.timestamp(),
        #                   end=datetime.fromisoformat(sort[2]['waktu']).timestamp(), position=.2))

        # list_perolehan: list[Perolehan] = [Perolehan(waktu=pemilih['waktu'], )]

        for i in range(10):
            waktu = random_date(start=waktu_mulai,
                                end=datetime.fromisoformat(
                                    sort[2]['waktu']), position=i / 10)

            print(waktu > waktu_mulai)
            # print(random_date(start=waktu_mulai.strftime("%m/%d/%y %I:%M%p"),
            #                   end=datetime.fromisoformat(
            #     sort[2]['waktu']).strftime("%m/%d/%y %I:%M%p"), position=i / 10))

        print(datetime.fromisoformat(sort[2]['waktu']) - waktu_mulai)

        # for kandidat in list.list_kandidat:

        # data: list[PemilihKotakSuara] = []

        # for i in range(len(filter)):
        #     fil = filter[i]
        #     pem = pemilih[i]
        #     data.append(PemilihKotakSuara(id=fil['id'], vote_nomor=fil['vote_nomor'],
        #                 waktu=fil['waktu'], nama=pem['nama'], username=pem['username']))

        # return data
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

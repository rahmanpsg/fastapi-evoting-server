
import json
from datetime import datetime
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, literal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.daftar_vote import DaftarVotes
from schemas.daftar_vote import DaftarVoteResponse


def add_voting(id_daftarVote: int, id_pemilih: int, vote_nomor: int, db: Session):
    try:
        daftar_vote = db.query(DaftarVotes).get(id_daftarVote)

        if not daftar_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Daftar Vote tidak ditemukan")

        result = db.execute(
            "SELECT JSON_SET(list_pemilih, REPLACE(JSON_UNQUOTE(JSON_SEARCH(list_pemilih, 'one', :id_pemilih, NULL, '$[*].id')), '.id', ''), JSON_OBJECT('id', ':id_pemilih','vote_nomor', ':vote_nomor', 'waktu', :waktu)) as update_list_pemilih, JSON_LENGTH(list_pemilih) as total_kandidat FROM vote_list where id = :id", {'id': id_daftarVote, 'id_pemilih': id_pemilih, 'vote_nomor': vote_nomor, 'waktu': datetime.now()}).first()

        if not result[0]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID Pemilih tidak terdaftar pada Daftar Vote")

        if vote_nomor > result.total_kandidat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Nomor Kandidat tidak terdaftar pada Daftar Vote")

        daftar_vote.list_pemilih = json.loads(result.update_list_pemilih)

        db.commit()

        return DaftarVoteResponse(message="Voting berhasil disimpan")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))

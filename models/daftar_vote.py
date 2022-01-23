from sqlalchemy import JSON, Boolean, Column, Date, DateTime,  Integer, String, Text, Time, func

from config.db import Base


class DaftarVotes(Base):
    __tablename__ = "vote_list"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    keterangan = Column(Text)
    tanggal_mulai = Column(Date())
    jam_mulai = Column(Time(timezone=True))
    tanggal_selesai = Column(Date())
    jam_selesai = Column(Time(timezone=True))
    list_kandidat = Column(JSON, default=[])
    list_pemilih = Column(JSON, default=[])
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

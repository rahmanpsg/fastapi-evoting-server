from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime,  Integer, String, Text, func

from config.db import Base


class Pemilihs(Base):
    __tablename__ = "pemilih"

    id = Column(Integer, primary_key=True, index=True)
    nik = Column(String(16), unique=True)
    nama = Column(String(100))
    username = Column(String(20), unique=True, index=True)
    password = Column(String(10))
    alamat = Column(Text)
    status = Column(Boolean, default=None)
    face_recognition = Column(Boolean, default=None)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

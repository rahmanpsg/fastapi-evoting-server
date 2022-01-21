
from sqlalchemy import Column, Integer, String, Text
from config.db import Base


class Kandidats(Base):
    __tablename__ = "kandidats"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    foto = Column(Text)
    keterangan = Column(Text)

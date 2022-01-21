from sqlalchemy import Boolean, Column,  Integer, String

from config.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    username = Column(String(20), unique=True, index=True)
    password = Column(String(10))
    role = Column(String(50), default="Pemilih")
    status = Column(Boolean, default=True)

# users = Table(
#     'users', meta,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('nama', String(100), index=True),
#     Column('username', String(20), unique=True, index=True),
#     Column('password', String(10)),
#     Column('level', String(50), default="Pemilih"),
#     Column('status', Boolean, default=True),
# )

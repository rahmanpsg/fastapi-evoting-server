from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import Users
from schemas.user import User, UserCreate, UserResponse
from services.error_handling import add_or_edit_exception


def get_all(db: Session):
    return db.query(Users).filter(Users.role != 'pemilih').all()


def create(req: UserCreate, db: Session):
    try:
        new_user = Users(
            nama=req.nama,
            username=req.username,
            password=req.password,
            role=req.role,
            status=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserResponse(message="User berhasil ditambahkan", item=new_user)

    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def update(id: int, req: UserCreate, db: Session):
    try:
        user = cek_user(id, db)
        user.update(req.dict())
        db.commit()

        return UserResponse(message="User berhasil diubah")
    except SQLAlchemyError as e:
        add_or_edit_exception(e)


async def delete(id: int,  db: Session):
    try:
        user = cek_user(id, db)

        user.delete(synchronize_session=False)
        db.commit()

        return UserResponse(message="User berhasil dihapus")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


def cek_user(id: int, db: Session):
    user = db.query(Users).filter(
        Users.id == id and Users.role == 'user')

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID User tidak ditemukan")

    return user

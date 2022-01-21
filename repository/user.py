from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import Users
from schemas.user import User


def get_all(db: Session):
    return db.query(Users).all()


def create(req: User, db: Session):
    try:
        new_user = Users(
            nama=req.nama,
            username=req.username,
            password='123ABC',
            role=req.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # return ApiResponse(error=False, message="User berhasil ditambahkan"), 201
        return 'User berhasil ditambahkan'
    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))

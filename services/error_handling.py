from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


def add_or_edit_exception(error: SQLAlchemyError):
    err_msg = error.args[0]

    print(err_msg)

    if 'Duplicate entry' in err_msg:
        field = ''
        if 'username' in err_msg:
            field = 'Username'
        elif 'nik' in err_msg:
            field = 'NIK'

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'{field} telah digunakan')

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail='Data gagal disimpan, terjadi masalah diserver')

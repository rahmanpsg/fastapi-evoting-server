from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.token import verify_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login/")


def get_current_user(data: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tidak dapat memverifikasi data credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_token(data, credentials_exception)

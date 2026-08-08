import jwt
from sqlalchemy.orm import Session
from models.user import UserModal
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.settings import settings
from datetime import datetime
from jwt.exceptions import InvalidTokenError
from utils.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def is_authenticated(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("_id")
        exp_time = int(data.get("exp"))

        current_time = datetime.now().timestamp()
        if current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")

        user = db.query(UserModal).filter(UserModal.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")

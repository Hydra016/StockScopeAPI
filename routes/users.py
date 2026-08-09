from fastapi import APIRouter, Depends, status
from models.user import UserModal
from controllers import users
from schemas.user import UserResponseSchema
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

user_router = APIRouter(prefix="/api/user", tags=["Users"])

@user_router.get('/current-user', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_current_user(user: UserModal = Depends(is_authenticated), db: Session = Depends(get_db)):
    return users.get_current_user(user, db)

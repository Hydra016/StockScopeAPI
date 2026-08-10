from fastapi import APIRouter, Depends, status, BackgroundTasks
from models.user import UserModal
from schemas.auth import LoginSchema
from controllers import auth
from schemas.user import UserSchema, UserResponseSchema
from utils.db import get_db
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])

@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(body: UserSchema, bg_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return auth.register_user(body, bg_tasks, db)

@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
    return auth.login_user(body, db)

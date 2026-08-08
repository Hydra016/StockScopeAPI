from fastapi import APIRouter, Depends, status
from models.user import UserModal
from services import auth
from schemas.user import UserResponseSchema
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

user_router = APIRouter(prefix="/api/user", tags=["Users"])

@user_router.get('/current-user', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_current_user(user: UserModal = Depends(is_authenticated), db: Session = Depends(get_db)):
    return auth.get_current_user(user, db)

# @user_router.get('/isAuth', response_model= UserResponseSchema, status_code=status.HTTP_200_OK)
# def is_auth(req: Request, db: Session = Depends(get_db)):
#     return controller.is_authenticated(req, db)
#
# @user_router.get('/', status_code=status.HTTP_200_OK)
# def get_all_users(db: Session = Depends(get_db)):
#     return controller.get_all_users(db)
#
# @user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     return controller.delete_user(user_id, db)

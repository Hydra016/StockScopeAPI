from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers import admin
# from models.user import UserModal
from schemas.user import UserResponseSchema
from utils.db import get_db
# from utils.helpers.authentication import is_authenticated

admin_router = APIRouter(prefix="/api/admin", tags=["Admin"])


@admin_router.get(
    "/users",
    response_model=List[UserResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    db: Session = Depends(get_db),
    # user: UserModal = Depends(is_authenticated), --> commenting out the authentication dependency for testing purposes
):
    return admin.get_all_users(db)


@admin_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    # user: UserModal = Depends(is_authenticated), --> commenting out the authentication dependency for testing purposes
):
    admin.delete_user(user_id, db)

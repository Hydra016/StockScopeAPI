from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import UserModal


def get_all_users(db: Session):
    return db.query(UserModal).all()


def delete_user(user_id: int, db: Session):
    user = db.query(UserModal).filter(UserModal.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )

    db.delete(user)
    db.commit()

from sqlalchemy.orm import Session
from models.user import UserModal

def get_current_user(user: UserModal, db: Session):
    return db.query(UserModal).get(user.id)
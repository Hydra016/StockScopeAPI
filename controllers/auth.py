from datetime import datetime, timedelta
import jwt
from schemas.auth import LoginSchema
from schemas.user import UserSchema
from sqlalchemy.orm import Session
from models.user import UserModal
from pwdlib import PasswordHash
from fastapi import HTTPException, status, BackgroundTasks
from utils.settings import settings
from services.mail import MailService
from utils.helpers.utility import generate_alphanumeric_code

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def verify_user(email: str, code: str, bg_tasks: BackgroundTasks):
    code = generate_alphanumeric_code()
    bg_tasks.add_task(MailService().send_verification_email, [email], code)

def register_user(body: UserSchema, bg_tasks: BackgroundTasks, db: Session):
    is_user = db.query(UserModal).filter(UserModal.username == body.username).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    is_user = db.query(UserModal).filter(UserModal.email == body.email).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    # hash_password = get_password_hash(body.password)

    # new_user = UserModal(
    #     username=body.username,
    #     email=body.email,
    #     hash_password=hash_password,
    #     name=body.name,
    # )

    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    code = generate_alphanumeric_code()
    bg_tasks.add_task(MailService().send_verification_email, [body.email], code)

    return { "message": "Please check your email for verification." }

def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModal).filter(UserModal.username == body.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"_id": user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)
    return { "token": token }
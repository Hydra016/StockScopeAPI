from fastapi import APIRouter, Depends, status
from models.user import UserModal
from controllers import stocks
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

stock_router = APIRouter(prefix="/api/stocks", tags=["Stocks"])

@stock_router.get('/quote', status_code=status.HTTP_200_OK)
def get_quote(db: Session = Depends(get_db), user: UserModal = Depends(is_authenticated)):
    return stocks.get_quote(db)

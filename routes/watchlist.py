from fastapi import APIRouter, Depends, status
from models.watchlist import WatchlistItemModel, WatchlistModel
from models.user import UserModal
from controllers import users
from schemas.watchlist import WatchlistResponseSchema, WatchlistSchema
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

watchlist_router = APIRouter(prefix="/api/watchlist", tags=["Watchlist"])

@watchlist_router.post('/create', status_code=status.HTTP_200_OK)
def create_watchlist(body: WatchlistSchema, user: WatchlistModel = Depends(is_authenticated), db: Session = Depends(get_db)):
    return users.create_watchlist(body, user, db)

from fastapi import APIRouter, Depends, status
from models.user import UserModal
from controllers import watchlist
from schemas.watchlist import WatchlistResponseSchema, WatchlistSchema
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

watchlist_router = APIRouter(prefix="/api/watchlist", tags=["Watchlist"])


@watchlist_router.post(
    "/create",
    response_model=WatchlistResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_watchlist(
    body: WatchlistSchema,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return watchlist.create_watchlist(body, user, db)

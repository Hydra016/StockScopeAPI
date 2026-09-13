from fastapi import APIRouter, Depends, status
from models.user import UserModal
from controllers import watchlist
from schemas.watchlist import (
    WatchlistItemResponseSchema,
    WatchlistItemSchema,
    WatchlistMarketResponse,
    WatchlistResponseSchema,
    WatchlistSchema,
    GetWatchlistItemSchema,
    UpdateWatchlistResponseSchema
)
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

watchlist_router = APIRouter(prefix="/api/watchlist", tags=["Watchlist"])

@watchlist_router.get(
    "/",
    response_model=list[WatchlistResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_watchlist_for_user(
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return watchlist.get_watchlist_for_user(user, db)

@watchlist_router.get(
    "/items",
    response_model=list[WatchlistItemResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_watchlist_items(
    body: GetWatchlistItemSchema,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return watchlist.get_watchlist_items(body, user, db)

@watchlist_router.get(
    "/{watchlist_id}/market",
    response_model=WatchlistMarketResponse,
    status_code=status.HTTP_200_OK,
)
async def get_watchlist_market(
    watchlist_id: int,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return await watchlist.get_watchlist_market(watchlist_id, user, db)


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


@watchlist_router.post(
    "/create-item",
    response_model=WatchlistItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_watchlist_item(
    body: WatchlistItemSchema,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return watchlist.create_watchlist_item(body, user, db)

@watchlist_router.put(
    "/update/{watchlist_id}",
    response_model=UpdateWatchlistResponseSchema,
    status_code=status.HTTP_200_OK
)
def update_watchlist(body: WatchlistSchema, watchlist_id: int,  user =  Depends(is_authenticated), db = Depends(get_db)):
    return watchlist.update_watchlist(body, watchlist_id, user, db)

@watchlist_router.delete(
    "/delete/{watchlist_id}",
    status_code=status.HTTP_200_OK,
)
def update_watchlist(watchlist_id: int,  user =  Depends(is_authenticated), db = Depends(get_db)):
    return watchlist.delete_watchlist(watchlist_id, user, db)

@watchlist_router.delete(
    "/{watchlist_id}/delete-item/{watchlist_item_id}",
    status_code=status.HTTP_200_OK,
)
def update_watchlist(watchlist_id: int, watchlist_item_id: int,  user =  Depends(is_authenticated), db = Depends(get_db)):
    return watchlist.delete_watchlist_item(watchlist_id, watchlist_item_id, user, db)
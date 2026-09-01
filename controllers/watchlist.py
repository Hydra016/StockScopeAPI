from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.watchlist import WatchlistModel, WatchlistItemModel
from schemas.watchlist import WatchlistSchema, WatchlistItemSchema
from models.user import UserModal


def create_watchlist(body: WatchlistSchema, user: UserModal, db: Session):
    is_watchlist = (
        db.query(WatchlistModel)
        .filter(WatchlistModel.name == body.name, WatchlistModel.user_id == user.id)
        .first()
    )

    if is_watchlist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Watchlist with this name already exists",
        )

    new_watchlist = WatchlistModel(name=body.name, user_id=user.id)
    db.add(new_watchlist)
    db.commit()
    db.refresh(new_watchlist)

    return new_watchlist

def create_watchlist_item(body: WatchlistItemSchema, user: UserModal, db: Session):
    watchlist = (
        db.query(WatchlistModel)
        .filter(WatchlistModel.id == body.watchlist_id, WatchlistModel.user_id == user.id)
        .first()
    )

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found",
        )

    existing_item = (
        db.query(WatchlistItemModel)
        .filter(
            WatchlistItemModel.watchlist_id == watchlist.id,
            WatchlistItemModel.symbol == body.symbol,
        )
        .first()
    )

    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol already exists in this watchlist",
        )

    new_item = WatchlistItemModel(watchlist_id=watchlist.id, symbol=body.symbol)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item 

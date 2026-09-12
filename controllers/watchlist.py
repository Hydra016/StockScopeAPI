from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.watchlist import WatchlistModel, WatchlistItemModel
from schemas.watchlist import (
    GetWatchlistItemSchema,
    WatchlistItemSchema,
    WatchlistResponseSchema,
    WatchlistSchema,
)
from models.user import UserModal
from controllers.stocks import get_quote


def get_owned_watchlist(watchlist_id: int, user: UserModal, db: Session) -> WatchlistModel:
    watchlist = (
        db.query(WatchlistModel)
        .filter(WatchlistModel.id == watchlist_id, WatchlistModel.user_id == user.id)
        .first()
    )

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found",
        )

    return watchlist

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
    watchlist = get_owned_watchlist(body.watchlist_id, user, db)

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

    new_item = WatchlistItemModel(watchlist_id=watchlist.id, symbol=body.symbol.strip().upper())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item 

def get_watchlist_for_user(user: UserModal, db: Session):
    rows = (
        db.query(WatchlistModel, func.count(WatchlistItemModel.id).label("item_count"))
        .outerjoin(
            WatchlistItemModel,
            WatchlistItemModel.watchlist_id == WatchlistModel.id,
        )
        .filter(WatchlistModel.user_id == user.id)
        .group_by(WatchlistModel.id)
        .all()
    )

    return [
        WatchlistResponseSchema(
            id=watchlist.id,
            name=watchlist.name,
            user_id=watchlist.user_id,
            created_at=watchlist.created_at,
            item_count=item_count,
        )
        for watchlist, item_count in rows
    ]

def get_watchlist_items(body: GetWatchlistItemSchema, user: UserModal, db: Session):
    watchlist = get_owned_watchlist(body.watchlist_id, user, db)

    return (
        db.query(WatchlistItemModel)
        .filter(WatchlistItemModel.watchlist_id == watchlist.id)
        .all()
    )

def update_watchlist(body: WatchlistSchema, watchlist_id: int, user: UserModal, db: Session):
    watchlist = get_owned_watchlist(watchlist_id, user, db)

    watchlist.updated_at = datetime.utcnow()

    body = body.model_dump()

    for field, value in body.items():
        setattr(watchlist, field, value)

    db.commit()
    db.refresh(watchlist)

    return watchlist

def delete_watchlist(watchlist_id: int, user: UserModal, db: Session):
    watchlist = get_owned_watchlist(watchlist_id, user, db)

    db.delete(watchlist)
    db.commit()

    return "Watchlist Deleted Successfully"

def delete_watchlist_item(watchlist_id: int, watchlist_item_id: int, user: UserModal, db: Session):
    get_owned_watchlist(watchlist_id, user, db)

    watchlist_item = db.query(WatchlistItemModel).filter(WatchlistItemModel.id == watchlist_item_id).first()

    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found",
        )

    db.delete(watchlist_item)
    db.commit()

    return "Watchlist Item Deleted Successfully"

async def get_watchlist_market(watchlist_id: int, user: UserModal, db: Session):
    watchlist = get_owned_watchlist(watchlist_id, user, db)

    watchlist_items = (
        db.query(WatchlistItemModel)
        .filter(WatchlistItemModel.watchlist_id == watchlist.id)
        .all()
    )

    stocks = []
    for item in watchlist_items:
        symbol = item.symbol.strip().upper()
        try:
            stock_data = await get_quote(symbol, db)
            stocks.append(
                {
                    "symbol": symbol,
                    "price": stock_data.data.current_price,
                    "change": stock_data.data.change,
                    "percent_change": stock_data.data.percent_change,
                }
            )
        except HTTPException:
            stocks.append(
                {
                    "symbol": symbol,
                    "price": None,
                    "change": None,
                    "percent_change": None,
                }
            )

    watchlist_market = {
        "id": watchlist.id,
        "name": watchlist.name,
        "stocks": stocks
    }

    return watchlist_market
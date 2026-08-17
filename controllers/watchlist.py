from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.watchlist import WatchlistModel
from schemas.watchlist import WatchlistSchema
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

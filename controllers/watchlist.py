from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.watchlist import WatchlistModal
from schemas.watchlist import WatchlistSchema
from models.user import UserModal

def create_watchlist(body: WatchlistSchema, user: UserModal, db: Session):
    is_watchlist = db.query(WatchlistModal).filter(WatchlistModal.name == body.name).first()
    
    if is_watchlist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Watchlist with this name already exists")
    
    data = body.model_dump()
    data["user_id"] = user.id
    new_watchlist = WatchlistModal(**data)
    db.add(new_watchlist)
    db.commit()
    db.refresh(new_watchlist)
    
    return new_watchlist
    
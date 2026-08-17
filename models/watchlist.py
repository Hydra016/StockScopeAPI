from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from utils.db import Base

class WatchlistModel(Base):
    __tablename__ = "watchlist_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
class WatchlistItemModel(Base):
    __tablename__ = "watchlist_item_table"

    id = Column(Integer, primary_key=True)
    watchlist_id = Column(Integer, ForeignKey("watchlist_table.id", ondelete="CASCADE"))
    symbol = Column(String)

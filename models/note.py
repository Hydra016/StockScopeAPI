from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float
from utils.db import Base

class StockNoteModel(Base):
    __tablename__ = "note_table"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))
    symbol = Column(String)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

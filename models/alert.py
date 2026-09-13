from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float
from utils.db import Base

class AlertModel(Base):
    __tablename__ = "alert_table"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))
    target_price = Column(Float, nullable=False)
    condition = Column(String, nullable=False)
    is_active = Column(Boolean)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)

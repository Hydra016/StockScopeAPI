from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WatchlistSchema(BaseModel):
    name: str


class WatchlistItemSchema(BaseModel):
    symbol: str


class WatchlistResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int
    created_at: datetime

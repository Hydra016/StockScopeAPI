from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WatchlistSchema(BaseModel):
    name: str


class WatchlistItemSchema(BaseModel):
    watchlist_id: int
    symbol: str

class GetWatchlistItemSchema(BaseModel):
    watchlist_id: int

class WatchlistResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int
    created_at: datetime
    item_count: int = 0


class WatchlistItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    watchlist_id: int
    symbol: str

class UpdateWatchlistResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    updated_at: datetime

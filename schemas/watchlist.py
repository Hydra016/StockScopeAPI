from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class WatchlistSchema(BaseModel):
    name: str
    
class WatchlistItemSchema(BaseModel):
    symbol: str

class WatchlistResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id = int
    name = str
    created_at = datetime
    updated_at = datetime


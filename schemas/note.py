from datetime import datetime
from pydantic import BaseModel, ConfigDict

class StockNoteCreateSchema(BaseModel):
    symbol: str
    title: str
    content: str

class StockNoteUpdateSchema(BaseModel):
    title: str
    content: str

class StockNoteResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    symbol: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    
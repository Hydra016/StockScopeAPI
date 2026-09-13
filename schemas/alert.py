from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class AlertCreateSchema(BaseModel):
    symbol: str
    target_price: float
    condition: str = Field(json_schema_extra={"enum": ["ABOVE", "BELOW"]})

class AlertUpdateSchema(BaseModel):
    target_price: Optional[float] = None
    condition: Optional[str] = Field(default=None, json_schema_extra={"enum": ["ABOVE", "BELOW"]})
    is_active: Optional[bool] = None 

class AlertResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    symbol: str
    target_price: float
    condition: str
    is_active: bool
    triggered_at: Optional[datetime] = None
    created_at: datetime
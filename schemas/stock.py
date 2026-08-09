from datetime import date, datetime, timezone
from typing import Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

class NewsItemSchema(BaseModel):
    category: str
    datetime: date
    headline: str
    id: int
    image: str
    related: str
    source: str
    summary: str
    url: HttpUrl

    @field_validator("datetime", mode="before")
    @classmethod
    def convert_timestamp(cls, value: Union[int, date]) -> date:
        if isinstance(value, int):
            return datetime.fromtimestamp(value, tz=timezone.utc).date()
        return value

class QuoteSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_price: float = Field(validation_alias="c")
    change: float = Field(validation_alias="d")
    percent_change: float = Field(validation_alias="dp")
    high: float = Field(validation_alias="h")
    low: float = Field(validation_alias="l")
    open: float = Field(validation_alias="o")
    previous_close: float = Field(validation_alias="pc")
    timestamp: int = Field(validation_alias="t")

class QuoteResponseSchema(BaseModel):
    data: QuoteSchema

class NewsResponseSchema(BaseModel):
    data: list[NewsItemSchema]

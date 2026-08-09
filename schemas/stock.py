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
    
class InsiderTransactionSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    share: int
    change: int
    filing_date: date = Field(validation_alias="filingDate")
    transaction_date: date = Field(validation_alias="transactionDate")
    transaction_code: str = Field(validation_alias="transactionCode")
    transaction_price: float = Field(validation_alias="transactionPrice")
    id: str
    # symbol: str --> not included in the response bcoz it is same as stock namez
    source: str
    is_derivative: bool = Field(validation_alias="isDerivative")
    # currency: str --> not included in the response bcoz it is empty in all the records
    
class FearGreedDataItemSchema(BaseModel):
    value: int
    value_classification: str
    timestamp: int
    time_until_update: Union[int, None] = None

class FearGreedMetadataSchema(BaseModel):
    error: Union[str, None] = None

class FearGreedIndexSchema(BaseModel):
    name: str
    data: list[FearGreedDataItemSchema]
    metadata: FearGreedMetadataSchema

class QuoteResponseSchema(BaseModel):
    data: QuoteSchema

class NewsResponseSchema(BaseModel):
    data: list[NewsItemSchema]
    
class InsiderTransactionResponseSchema(BaseModel):
    data: list[InsiderTransactionSchema]
    
class MarketSentimentResponseSchema(BaseModel):
    data: FearGreedIndexSchema

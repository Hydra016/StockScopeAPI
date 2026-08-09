from datetime import date

from sqlalchemy.orm import Session
from schemas.stock import (
    NewsItemSchema,
    NewsResponseSchema,
    QuoteResponseSchema,
    QuoteSchema,
)
from services.finnhup import FinnhubService


async def get_quote(stock: str, db: Session):
    if not stock:
        raise ValueError("Stock symbol is required")

    res = await FinnhubService(stock=stock).get_stock_data()
    return QuoteResponseSchema(data=QuoteSchema.model_validate(res))


async def get_news(stock: str, from_date: date, to_date: date, db: Session):
    if not stock:
        raise ValueError("Stock symbol is required")

    res = await FinnhubService(stock=stock).get_stock_news(from_date, to_date)
    return NewsResponseSchema(data=[NewsItemSchema.model_validate(item) for item in res])

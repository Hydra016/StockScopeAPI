from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.stock import (
    InsiderTransactionResponseSchema,
    InsiderTransactionSchema,
    NewsItemSchema,
    NewsResponseSchema,
    QuoteResponseSchema,
    QuoteSchema,
    MarketSentimentResponseSchema,
    FearGreedIndexSchema
)
from services.finnhup import FinnhubService
from services.sentiment import MarketSentimentService

async def get_quote(stock: str, db: Session):
    if not stock:
        raise ValueError("Stock symbol is required")

    try:
        res = await FinnhubService(stock=stock.strip().upper()).get_stock_data()
        return QuoteResponseSchema(data=QuoteSchema.model_validate(res))
    except HTTPException:
        raise
    except Exception as exc:
        print(f"get_quote failed for {stock}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API can not be reached",
        )

async def get_news(stock: str, from_date: date, to_date: date, db: Session):
    if not stock:
        raise ValueError("Stock symbol is required")

    try:
        res = await FinnhubService(stock=stock).get_stock_news(from_date, to_date)
        return NewsResponseSchema(data=[NewsItemSchema.model_validate(item) for item in res])
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API can not be reached",
        )
        
async def get_insider_info(stock: str, db: Session):
    if not stock:
        raise ValueError("Stock symbol is required")

    try:
        res = await FinnhubService(stock=stock).get_insider_info()
        return InsiderTransactionResponseSchema(
        data=[InsiderTransactionSchema.model_validate(item) for item in res.get("data", [])]
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API can not be reached",
        )
    
async def get_market_sentiment():
    try:
        res = await MarketSentimentService().get_stock_data()
        return MarketSentimentResponseSchema(data=FearGreedIndexSchema.model_validate(res))
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API can not be reached",
        )

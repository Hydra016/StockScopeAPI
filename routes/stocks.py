from datetime import date
from schemas.stock import QuoteResponseSchema, NewsResponseSchema, InsiderTransactionResponseSchema, MarketSentimentResponseSchema
from fastapi import APIRouter, Depends, status
from models.user import UserModal
from controllers import stocks
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated

stock_router = APIRouter(prefix="/api/stocks", tags=["Stocks"])

@stock_router.get('/quote/{stock}', response_model= QuoteResponseSchema, status_code=status.HTTP_200_OK)
async def get_quote(stock: str, db: Session = Depends(get_db), user: UserModal = Depends(is_authenticated)):
    return await stocks.get_quote(stock, db)

@stock_router.get('/news/{stock}', response_model= NewsResponseSchema, status_code=status.HTTP_200_OK)
async def get_news(stock: str, from_date: date, to_date: date, db: Session = Depends(get_db), user: UserModal = Depends(is_authenticated)):
    return await stocks.get_news(stock, from_date, to_date, db)

@stock_router.get('/insider-info/{stock}', response_model= InsiderTransactionResponseSchema, status_code=status.HTTP_200_OK)
async def get_insider_info(stock: str, db: Session = Depends(get_db), user: UserModal = Depends(is_authenticated)):
    return await stocks.get_insider_info(stock, db)

@stock_router.get('/market-sentiment', response_model= MarketSentimentResponseSchema, status_code=status.HTTP_200_OK)
async def get_market_sentiment(user: UserModal = Depends(is_authenticated)):
    return await stocks.get_market_sentiment()
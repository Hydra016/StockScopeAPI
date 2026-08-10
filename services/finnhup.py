from datetime import date
import httpx
from utils.constants import FINNHUB_BASE_URL
from utils.settings import settings

class FinnhubService:
    def __init__(self, stock, api_key: str = settings.FINNHUB_API_KEY, base_url: str = FINNHUB_BASE_URL, timeout: float = 10.0):
        self._api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.stock = stock
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={"X-Finnhub-Token": self.api_key},
        )
        
    @property
    def api_key(self):
        return self._api_key
    
    @property
    def client(self):
        return self._client
        
    async def get_stock_data(self):
        response = await self.client.get("/quote", params={"symbol": self.stock})
        response.raise_for_status()
        return response.json()
    
    async def get_stock_news(self, from_date: date, to_date: date):
        response = await self.client.get("/company-news", params={"symbol": self.stock, "from": from_date.isoformat(), "to": to_date.isoformat()})
        response.raise_for_status()
        return response.json()
    
    async def get_insider_info(self):
        response = await self.client.get("/stock/insider-transactions", params={"symbol": self.stock})
        response.raise_for_status()
        return response.json()

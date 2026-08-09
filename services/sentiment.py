from datetime import date
import httpx
from utils.constants import FNG_BASE_URL

class MarketSentimentService:
    def __init__(self, base_url: str = FNG_BASE_URL, timeout: float = 10.0):
        self.base_url = base_url
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )
    
    @property
    def client(self):
        return self._client
        
    async def get_stock_data(self):
        response = await self.client.get("/fng/")
        response.raise_for_status()
        return response.json()

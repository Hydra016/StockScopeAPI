import httpx
from utils.constants import FINNHUB_BASE_URL

class FinnhubService:
    def __init__(self, api_key: str, base_url: str = FINNHUB_BASE_URL, timeout: float = 10.0, stock: str = 'AMZN'):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.stock = stock
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={"X-Finnhub-Token": self.api_key},
        )

    async def get_stock_data(self):
        url = f"{self.base_url}/quote?symbol={self.stock}&token={self.api_key}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
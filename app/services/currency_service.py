import httpx
from app.core.config import settings

async def get_conversion_rate(from_currency: str, to_currency: str) -> float:
    async with httpx.AsyncClient() as client:
        params = {
            "apikey": settings.currency_api_key,
            "currencies": to_currency,
            "base_currency": from_currency,
        }
        response = await client.get(settings.currency_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["data"][to_currency]["value"]

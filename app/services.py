from typing import Any

import httpx
from sqlalchemy import select

from .config import settings
from .models import URLMapping
from .database import get_db_session
from .utils import generate_short_id


async def create_short_url(original_url: str) -> str:
    async with get_db_session() as session:
        short_id = generate_short_id()

        # Проверка уникальности
        stmt = select(URLMapping).where(URLMapping.short_id == short_id)
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        while existing:
            short_id = generate_short_id()
            stmt = select(URLMapping).where(URLMapping.short_id == short_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

        url_mapping = URLMapping(
            short_id=short_id,
            original_url=original_url
        )
        session.add(url_mapping)
        await session.commit()

        return short_id


async def get_original_url(short_id: str) -> Any | None:
    async with get_db_session() as session:
        stmt = select(URLMapping).where(URLMapping.short_id == short_id)
        result = await session.execute(stmt)
        url_mapping = result.scalar_one_or_none()

        if not url_mapping:
            return None

        return url_mapping.original_url


async def verify_url_availability(url: str):
    try:
        async with httpx.AsyncClient(timeout=settings.SERVICE_TIMEOUT) as client:
            response = await client.head(url)
            response.raise_for_status()
            return True
    except Exception as e:
        print(f"URL verification failed for {url}: {str(e)}")
        return False


async def fetch_url_data(url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=settings.SERVICE_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()

            return {
                "status": response.status_code,
                "headers": dict(response.headers),
                "content": response.text[:1000] + "..." if len(response.text) > 1000 else response.text
            }
    except httpx.HTTPError as e:
        raise ValueError(f"External request failed: {str(e)}")
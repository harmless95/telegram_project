from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def execute_query(session: AsyncSession, sql: str) -> Any:
    try:
        result = await session.execute(text(sql))
        value = result.scalar()
        return value
    except Exception as ex:
        raise

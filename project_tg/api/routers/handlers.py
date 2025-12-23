import asyncio
import logging
from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from api.Dependencies import execute_query, generate_sql, conn_client
from api.Dependencies.async_logging import log_user_query, log_query_result, log_error
from core.model import db_helper_conn

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!\n"
        f"📱 ID: <code>{message.from_user.id}</code>"
    )


@router.message(F.text)
async def handler_query(message: Message):
    async with db_helper_conn.get_generator_session() as session:
        user_text = message.text
        try:
            asyncio.create_task(log_user_query(message))
            client = await conn_client()

            sql = await generate_sql(query=user_text, client=client)
            if not sql or "SELECT" not in sql.upper():
                await message.answer("❌ Не удалось сгенерировать SQL.")
                return

            await message.answer("🔄 Выполняю запрос...")

            result = await asyncio.wait_for(
                execute_query(session=session, sql=sql), timeout=10
            )

            await message.answer(f"✅ Результат: <code>{result or 0}</code>")
            asyncio.create_task(
                log_query_result(message=message, sql=sql, result=result)
            )

        except Exception as ex:
            asyncio.create_task(log_error(message=message, error=ex))
            await message.answer(
                "Произошла ошибка при обработке запроса. Попробуйте ещё раз позже."
            )

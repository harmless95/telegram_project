from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from api.Dependencies import execute_query, generate_sql, conn_client
from core.model import db_helper_conn

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
            client = await conn_client()

            sql = await generate_sql(query=user_text, client=client)
            if not sql or "SELECT" not in sql.upper():
                await message.answer(
                    "Не удалось распознать запрос, попробуйте сформулировать иначе."
                )
                return
            result = await execute_query(session=session, sql=sql)

            if result is None:
                result = 0
            await message.answer(str(result))

        except Exception as ex:
            await message.answer(
                "Произошла ошибка при обработке запроса. Попробуйте ещё раз позже."
            )

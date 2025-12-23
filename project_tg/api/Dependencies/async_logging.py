import logging
from aiogram.types import Message


logger = logging.getLogger(__name__)


async def log_user_query(message: Message):
    try:
        logger.info(
            f"Пользователь {message.from_user.id} ({message.from_user.full_name}): {message.text}"
        )
    except Exception as ex:
        logger.error(f"Ошибка логирования: {ex}")


async def log_query_result(message: Message, sql, result):
    try:
        logger.info(
            f"Пользователь {message.from_user.id}, Запрос: {message.text}, SQL: {sql}, Результат: {result}"
        )
    except Exception as ex:
        logger.error(f"Ошибка логирования: {ex}")


async def log_error(message: Message, error):
    try:
        logger.error(f"Пользователь {message.from_user.id}, Ошибка: {error}")
    except Exception as ex:
        logger.error(f"Ошибка логирования: {ex}")

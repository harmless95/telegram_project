import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import setting
from api.routers.handlers import router
from core.core_logging import loging_constructor


async def main() -> None:
    loop = asyncio.get_running_loop()
    loop.set_task_factory(lambda loop, coro: loging_constructor(loop=loop, coro=coro))
    bot = Bot(
        token=setting.t_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router=router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

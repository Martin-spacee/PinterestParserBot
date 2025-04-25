from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import Config
from handlers.user_handlers import router_1
import asyncio


async def main():
    config = Config('bot/.env')
    storage = MemoryStorage()
    bot = Bot(config.bot_token)
    dp = Dispatcher(storage=storage)

    dp.include_router(router=router_1)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

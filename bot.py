import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import (download_handler,
                      upload_handler,
                      start_handler,
                      upload_from_url_handler)

from settings import settings

logging.basicConfig(level=logging.INFO)


async def main() -> None:

    bot = Bot(settings.TOKEN.get_secret_value(), parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher()

    dp.include_routers(download_handler.router,
                       upload_handler.router,
                       upload_from_url_handler.router,
                       start_handler.router
                       )

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


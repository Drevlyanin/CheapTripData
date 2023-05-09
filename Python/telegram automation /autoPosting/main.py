import handlers
import asyncio
import logging
from utils.loader import dp, bot


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.warning('bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

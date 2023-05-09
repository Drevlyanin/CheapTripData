import asyncio
import aioschedule


async def add_task(func):
    aioschedule.every(5).seconds.do(func)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def clear_tasks():
    aioschedule.clear()

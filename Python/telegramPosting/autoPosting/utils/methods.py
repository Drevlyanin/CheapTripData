import asyncio
import aioschedule


async def add_task(func, text='Content', photo=None):
    aioschedule.every(5).seconds.do(func, text, photo)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def clear_tasks():
    aioschedule.clear()

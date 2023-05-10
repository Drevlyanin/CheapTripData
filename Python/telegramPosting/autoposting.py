import json
import asyncio
import aiogram


async def main():
    bot_token = ""
    channel_id = ""

    bot = aiogram.Bot(token=bot_token)
    dp = aiogram.Dispatcher(bot)

    with open('posts.json', 'r') as f:
        data = json.load(f)
        posts = data["posts"]

    i = 0

    while True:
        text = posts[i]["text"]
        photo_path = posts[i]["photo_url"]

        try:
            await bot.send_photo(chat_id=channel_id, photo=open(photo_path, 'rb'))
            await bot.send_message(chat_id=channel_id, text=text)

        except Exception as e:
            print(f"Error sending message: {e}")

        i = (i + 1) % len(posts)
        await asyncio.sleep(60 * 60 * 24)

    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.get_session()
    await bot.close()

asyncio.run(main())

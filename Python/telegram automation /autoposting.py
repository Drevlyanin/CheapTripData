import json
import asyncio
import aiogram



async def main():

    bot = aiogram.Bot(token="")

    # Create a Dispatcher object for the bot
    dp = aiogram.Dispatcher(bot)

    # Load the data from the JSON file
    with open('posts.json', 'r') as f:
        data = json.load(f)

    # Extract the text and photo URL from the data
    text = data["text"]
    photo_path = data["photo_url"]

    try:
        # Send the photo with the text as the caption to the specified chat ID
        await bot.send_photo(chat_id="", photo=open(photo_path, 'rb'), caption=text)

    except Exception as e:
        # If there's an error, print it out to the console
        print(f"Error sending message: {e}")

    # Close the storage of the dispatcher. Get the session of the bot and close it
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.get_session()
    await bot.close()

asyncio.run(main())

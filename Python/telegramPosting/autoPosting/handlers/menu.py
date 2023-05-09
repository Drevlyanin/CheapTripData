import json
import logging

from aiogram.dispatcher.filters import Text
from aiogram import types

import keyboards.default as default
from utils import methods
from utils.config import config
from utils.loader import dp, bot


async def task(text='Content', photo=None):
    if photo:
        await bot.send_photo(chat_id=config.channel_id.get_secret_value(), photo=photo, caption=text)
        return
    await bot.send_message(chat_id=config.channel_id.get_secret_value(), text=text)


def get_post(name=None):
    try:
        with open(f'files/city_descriptions/{name}.json') as f:
            city_description = json.load(f)
        f.close()
        with open(f'files/city_descriptions/{name}.json') as f:
            city_description = json.load(f)
        f.close()

        print(city_description)
    except Exception as e:
        logging.warning('Error: ', e)


@dp.message(Text(text='Start Posting'))
async def cmd_ecn(message: types.Message):
    await message.answer(text='Posting started!', reply_markup=default.keyboard_stopPost())
    await methods.add_task(task, text='', photo='files/img1.jpg')


@dp.message(Text(text='Stop Posting'))
async def cmd_ecn(message: types.Message):
    await message.answer(text='Posting stopped!', reply_markup=default.keyboard_post())
    await methods.clear_tasks()

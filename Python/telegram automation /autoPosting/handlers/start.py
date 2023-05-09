from aiogram.dispatcher.filters import Text

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.loader import dp, bot
from utils import methods
from utils.config import config


def keyboard_post():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Start Posting'))
    return builder.as_markup(resize_keyboard=True)


def keyboard_stopPost():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Stop Posting'))
    return builder.as_markup(resize_keyboard=True)


async def task(text='Content', photo=None):
    if photo:
        await bot.send_photo(chat_id=config.channel_id.get_secret_value(), photo=photo, caption=text)
        return
    await bot.send_message(chat_id=config.channel_id.get_secret_value(), text=text)


@dp.message(commands='start')
@dp.callback_query(text='start')
async def cmd_start(message: types.Message):
    await message.answer(text=f'Hello, {message.from_user.username}!', reply_markup=keyboard_post())
    # await methods.add_task(task)


@dp.message(Text(text='Start Posting'))
async def cmd_ecn(message: types.Message):
    await message.answer(text='Posting started!', reply_markup=keyboard_stopPost())
    await methods.add_task(task)


@dp.message(Text(text='Stop Posting'))
async def cmd_ecn(message: types.Message):
    await message.answer(text='Posting stopped!', reply_markup=keyboard_post())
    await methods.clear_tasks()

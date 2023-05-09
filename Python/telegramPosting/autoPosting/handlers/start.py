from aiogram import types

import keyboards.default as default
from utils.loader import dp, bot


@dp.message(commands='start')
@dp.callback_query(text='start')
async def cmd_start(message: types.Message):
    await message.answer(text=f'Hello, {message.from_user.username}!', reply_markup=default.keyboard_post())

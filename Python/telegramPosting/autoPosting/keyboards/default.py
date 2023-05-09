from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def keyboard_post():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Start Posting'))
    return builder.as_markup(resize_keyboard=True)


def keyboard_stopPost():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Stop Posting'))
    return builder.as_markup(resize_keyboard=True)

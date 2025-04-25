from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from lexicon.lexicon import dct


def get_inline_keyboard(typ=None, **kwargs):
    keyboard = InlineKeyboardBuilder()

    for text, val in kwargs.items():
        keyboard.row(InlineKeyboardButton(text=dct[text] if text in dct else text, url=val), width=1) if typ == 'url' else \
            keyboard.row(InlineKeyboardButton(text=dct[text] if text in dct else text, callback_data=text), width=1)
    if typ == 'url':
        keyboard.row(InlineKeyboardButton(text='Проверить', callback_data='check'))
    return keyboard.as_markup()

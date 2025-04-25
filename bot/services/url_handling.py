import requests
from pyquery import PyQuery
from aiogram import Bot
from lexicon.lexicon import LEXICON_RU, link
from keyboards.inline_keyboard import get_inline_keyboard
from aiogram.types import Message



def get_url_of_photo_or_video(link):
    request_pinterest = requests.get(link)
    if request_pinterest.status_code != 200: return None

    request_experts = requests.post('https://www.expertsphp.com/download.php', data={'url': request_pinterest.url})
    request_content = str(request_experts.content, 'utf-8')
    download_url = PyQuery(request_content)('table.table-condensed')('tbody')('td')('a').attr('href')
    return download_url


async def user_in_channel(bot: Bot, user_id):
    in_channel = await bot.get_chat_member(chat_id='@godblesssusalll', user_id=user_id)
    return in_channel.status != 'left'


async def send_error(message: Message):
    kb = get_inline_keyboard('url', subscribe=link)
    await message.answer(LEXICON_RU['not_subscribed'], reply_markup=kb)
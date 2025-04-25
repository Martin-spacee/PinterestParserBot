from lexicon.lexicon import LEXICON_RU, link
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state.state import FSMGetContent
from services.url_handling import get_url_of_photo_or_video, user_in_channel, send_error
from keyboards.inline_keyboard import get_inline_keyboard
from aiogram import Bot


router_1 = Router()


@router_1.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    await message.answer(LEXICON_RU['/start'])


@router_1.message(Command(commands='help'))
async def help_command(message: Message, state: FSMContext, bot: Bot):
    kb = get_inline_keyboard('url', subscribe=link)

    if await user_in_channel(bot, message.from_user.id):
        await message.answer(LEXICON_RU['/help_2'])
    else:
        await message.answer(LEXICON_RU['/help_1'], reply_markup=kb)
        await state.set_state(FSMGetContent.subscribe)


@router_1.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_command(message: Message, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, message.from_user.id):
        await state.set_state(default_state)
        await message.answer(LEXICON_RU['negative_answer'])
    else:
        await send_error(message)
        await state.set_state(FSMGetContent.subscribe)


@router_1.message(Command(commands='download_content'), StateFilter(default_state))
async def download_content_command(message: Message, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, message.from_user.id):
        await message.answer(LEXICON_RU['/download_content'])
        await state.set_state(FSMGetContent.check_link)
    else:
        await send_error(message)
        await state.set_state(FSMGetContent.subscribe)


@router_1.callback_query(lambda x: x.data == 'check', StateFilter(FSMGetContent.subscribe))
async def check_subscribe_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, callback.from_user.id):
        await callback.message.edit_text(LEXICON_RU['passed_the_test'])
        await state.set_state(FSMGetContent.check_link)
    else:
        await callback.answer(LEXICON_RU['failed_the_test'])


@router_1.message(StateFilter(FSMGetContent.subscribe))
async def any_command(message: Message):
    kb = get_inline_keyboard('url', subscribe=link)

    await message.answer(LEXICON_RU['not_subscribed'], reply_markup=kb)


@router_1.message(
    lambda x: x.text and ('pinterest.com' in x.text or 'pin.it' in x.text),
    StateFilter(FSMGetContent.check_link))
async def get_link(message: Message, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, message.from_user.id):
        kb = get_inline_keyboard(yes='Да', no='Нет')
        photo_or_video = get_url_of_photo_or_video(message.text)

        if photo_or_video is None:
            await message.answer(LEXICON_RU['invalid_link'])
        else:
            if '.mp4' in str(photo_or_video):
                await message.answer(LEXICON_RU['get_video'])
                await bot.send_video(chat_id=message.chat.id, video=photo_or_video)
            else:
                await message.answer(LEXICON_RU['get_photo'])
                await bot.send_photo(chat_id=message.chat.id, photo=photo_or_video)
            await state.set_state(FSMGetContent.user_answer)
            await message.answer(LEXICON_RU['want_more'], reply_markup=kb)
    else:
        await state.set_state(FSMGetContent.subscribe)
        await send_error(message)


@router_1.message(StateFilter(FSMGetContent.check_link))
async def wrong_link(message: Message, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, message.from_user.id):
        await message.answer(LEXICON_RU['not_a_link'])
    else:
        await state.set_state(FSMGetContent.subscribe)
        await send_error(message)


@router_1.callback_query(lambda x: x.data == 'yes', StateFilter(FSMGetContent.user_answer))
async def positive_answer(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, callback.message.from_user.id):
        await callback.message.edit_text(LEXICON_RU['positive_answer'])
        await state.set_state(FSMGetContent.check_link)
    else:
        await state.set_state(FSMGetContent.subscribe)
        await send_error(callback.message)


@router_1.callback_query(lambda x: x.data == 'no', StateFilter(FSMGetContent.user_answer))
async def negative_answer(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if await user_in_channel(bot, callback.message.from_user.id):
        await callback.message.edit_text(LEXICON_RU['negative_answer'])
        await state.clear()
    else:
        await state.set_state(FSMGetContent.subscribe)
        await send_error(callback.message)


@router_1.message(StateFilter(FSMGetContent.user_answer))
async def dont_understand(message: Message):
    kb = get_inline_keyboard(yes='Да', no='Нет')
    await message.answer(LEXICON_RU['dont_understand_2'], reply_markup=kb)


@router_1.message()
async def any_answer(message: Message, bot: Bot, state: FSMContext):
    if await user_in_channel(bot, message.from_user.id):
        await message.answer(LEXICON_RU['dont_understand'])
    else:
        await state.set_state(FSMGetContent.subscribe)
        await send_error(message)

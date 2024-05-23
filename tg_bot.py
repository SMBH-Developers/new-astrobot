import asyncio

from aiogram import Bot, Dispatcher, executor, types, exceptions
from aiogram.utils import markdown
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from src.config import Texts
from src.common import settings
from src.keyboards import Markups, MenuButton
from src.models import db, db_sendings


storage = RedisStorage2(db=settings.redis_db, pool_size=40)
bot = Bot(settings.tg_token)
dp = Dispatcher(bot, storage=storage)
ADMIN_IDS = (1188441997, 791363343)


BF_PEOPLE = [791363343, 923202245, 1633990660, 1188441997, 627568042]


class Form(StatesGroup):
    age = State()


@dp.message_handler(commands=['start'], state='*')
async def start_mes(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(Texts.welcome_text, reply_markup=Markups.welcome_mrkup, parse_mode='html')
    await db.registrate_if_not_exists(message.from_user.id)
    await asyncio.sleep(1)
    await message.answer(Texts.menu, reply_markup=MenuButton.main_menu_mrkup, parse_mode='html')


@dp.callback_query_handler(lambda call: call.data == 'welcome:purpose')
async def process_callback_purpose(callback_query: types.CallbackQuery) -> None:
    inline_button = types.InlineKeyboardMarkup()
    inline_button.add(types.InlineKeyboardButton(text='🥳 Да, конечно ', callback_data='yes'))
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.purpose_text, reply_markup=inline_button, parse_mode='html')


@dp.callback_query_handler(lambda call: call.data == 'welcome:horoscope')
async def process_callback_horoscope(callback_query: types.CallbackQuery) -> None:
    inline_button = types.InlineKeyboardMarkup()
    inline_button.add(types.InlineKeyboardButton(text='🤗 Начнем', callback_data='start'))
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.horoscope_text, reply_markup=inline_button, parse_mode='html')


@dp.callback_query_handler(lambda call: call.data == 'welcome:compatibility')
async def process_callback_compatibility(callback_query: types.CallbackQuery) -> None:
    inline_button = types.InlineKeyboardMarkup()
    inline_button.add(types.InlineKeyboardButton(text='😍 Разобрать сферу отношений', callback_data='relationship'))
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.compatibility_text, reply_markup=inline_button, parse_mode='html')


@dp.callback_query_handler(lambda call: call.data == 'welcome:wealth')
async def process_callback_wealth(callback_query: types.CallbackQuery) -> None:
    inline_button = types.InlineKeyboardMarkup()
    inline_button.add(types.InlineKeyboardButton(text='😉 Конечно', callback_data='sure'))
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.wealth_text, reply_markup=inline_button, parse_mode='html')


@dp.message_handler(lambda message: message.text in ['📝 Записаться к астрологу', '✨ Все об астрологии'])
async def start_mes(message: types.Message) -> None:
    if message.text == '📝 Записаться к астрологу':
        # await message.answer(Texts.get_birthday)
        await Form.age.set()
    elif message.text == '✨ Все об астрологии':
        await message.answer(Texts.advice_day, reply_markup=Markups.main_menu_mrkup)


@dp.callback_query_handler(lambda call: call.data == 'main:map')
async def process_callback_map(callback_query: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.map_text)


@dp.callback_query_handler(lambda call: call.data == 'main:day')
async def process_callback_day(callback_query: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.advice_day)


@dp.callback_query_handler(lambda call: call.data in ['yes', 'start', 'relationship', 'sure'])
async def process_callback_yes(callback_query: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(Texts.get_birthday_1)
    await Form.age.set()


@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await message.answer(Texts.finish_text)
    await state.finish()


@dp.message_handler(lambda message: message.from_user.id in ADMIN_IDS, state='*', commands=['admin'])
@logger.catch
async def admin_menu(message: types.Message) -> None:
    await bot.send_message(message.chat.id, text='Выберите действие', reply_markup=Markups.admin_mrkup)


@dp.callback_query_handler(lambda call: call.from_user.id in ADMIN_IDS and call.data.startswith('Admin'), state='*')
@logger.catch
async def admin_calls(call: types.CallbackQuery) -> None:
    action = '_'.join(call.data.split('_')[1:])
    if action == 'Users_Total':
        await call.message.edit_text(text=f'Пользователей всего: {await db.get_count_all_users()}',
                                     reply_markup=Markups.back_admin_mrkup)

    elif action == 'Users_For_TODAY':
        await call.message.edit_text(text=f'Пользователей за сегодня: {await db.users_for_today()}',
                                     reply_markup=Markups.back_admin_mrkup)

    elif action == 'BACK':
        await call.message.edit_text(text='Выберите действие', reply_markup=Markups.admin_mrkup)


# async def sending_messages_2h():
#     while True:
#         await asyncio.sleep(7)

#         text_for_2h_autosending = f"🤩 Спешу сообщить, что {markdown.hbold('остается всего 6 бесплатных мест')}, чтобы получить бесплатную диагностику от чакролога🧘‍♀️. \n\nНе откладывайте свой счастье на потом😊. Забронировать за собой бесплатную чакральную диагностику, просто написав эксперту Адель @soul_mento в личные сообщения свою дату рождения."
#         mrkup = types.InlineKeyboardMarkup()
#         mrkup.add(types.InlineKeyboardButton("Впустить счастье ✨", url="https://t.me/soul_mento"))

#         users = await db_sendings.get_users_2h_autosending()
#         for user in users:
#             try:
#                 await bot.send_message(user, text_for_2h_autosending, parse_mode='html', reply_markup=mrkup)
#                 logger.info(f'ID: {user}. Got 2h_autosending')
#                 await db_sendings.mark_got_2h_autosending(user)
#                 await asyncio.sleep(0.2)
#             except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.ChatNotFound):
#                 logger.error(f'ID: {user}. DELETED')
#                 await db.delete_user(user)
#             except Exception as ex:
#                 logger.error(f'got error: {ex}')


# async def sending_message_24_h():
#     while True:
#         await asyncio.sleep(12)

#         text_autosending_24h = f"🌖Здравствуйте, сегодня {markdown.hbold('Луна находится в самой благоприятной фазе')}, при которой можно сделать наиболее {markdown.hbold('точный индивидуальный астрологический разбор')} по натальной карте. В честь этого события — астролог {markdown.hbold('Вера подготовит для Вас бесплатный разбор.')}\n\n🧘‍♀️В нем Вы узнаете о том, какую {markdown.hbold('дорогу советуют выбрать звезды,')} как можно решить {markdown.hbold('текущие жизненные проблемы')} и избежать {markdown.hbold('дальнейших неудач')} в своем жизненном пути\n\nДля получения необходимо {markdown.hbold('написать дату')} и {markdown.hbold('место своего рождения')} в личные сообщения — @your_mentoor 👈\n\n{markdown.hbold('🔮Количество бесплатных мест ограничено!')}"
#         mrkup = types.InlineKeyboardMarkup()
#         mrkup.add(types.InlineKeyboardButton("🔆Бесплатный астрологический разбор", url="https://t.me/soul_mento"))

#         users = await db_sendings.get_users_24h_autosending()
#         for user in users:
#             try:
#                 await bot.send_message(user, text_autosending_24h, parse_mode='html', reply_markup=mrkup)
#                 logger.info(f'ID: {user}. Got autosending_24h')
#                 await db_sendings.mark_got_24h_autosending(user)
#                 await asyncio.sleep(0.2)
#             except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.ChatNotFound):
#                 logger.error(f'ID: {user}. DELETED')
#                 await db.delete_user(user)
#             except Exception as ex:
#                 logger.error(f'got error: {ex}')


# async def sending_message_48_h():
#     while True:
#         await asyncio.sleep(12)

#         text_autosending_48h = f"🧚‍♂️Здравствуйте, в {markdown.hbold('этот замечательный день')} число моих {markdown.hbold('учеников')}, получивших {markdown.hbold('астрологическую консультацию')} в этом году — {markdown.hbold('превысило 1.500 человек')}\n\nВ честь такого {markdown.hbold('важного события')}, я хочу сделать {markdown.hbold('Вам подарок')} и сделать {markdown.hbold('бесплатный астрологический разбор🎉')}\n\nДля получения {markdown.hbold('бесплатного разбора')} — {markdown.hbold('напишите')} мне в личные сообщения {markdown.hbold('дату рождения')} — @your_mentoor👈\n\n🪄{markdown.hbold('Бесплатный разбор только для первых 10 написавших')}"
#         mrkup = types.InlineKeyboardMarkup()
#         mrkup.add(types.InlineKeyboardButton("Забрать подарок🎁", url="https://t.me/soul_mento"))

#         users_for_autosending_1 = await db_sendings.get_users_48h_autosending()
#         for user in users_for_autosending_1:
#             try:
#                 await bot.send_message(user, text_autosending_48h, parse_mode='html', reply_markup=mrkup)
#                 logger.info(f'ID: {user}. Got autosending_text_48h')
#                 await db_sendings.mark_got_48h_autosending(user)
#                 await asyncio.sleep(0.2)
#             except (exceptions.BotBlocked, exceptions.UserDeactivated):
#                 logger.error(f'ID: {user}. DELETED')
#                 await db.delete_user(user)
#             except Exception as ex:
#                 logger.error(f'got error: {ex}')


# async def sending_message_72h():
#     while True:
#         await asyncio.sleep(12)

#         text = f'🪐Здравствуйте, хочу сообщить, что после {markdown.hbold("Ваших многочисленных просьб")} - я {markdown.hbold("открываю второй поток")} и {markdown.hbold("хочу подарить 15-ти")} счастливчикам {markdown.hbold("бесплатный астрологический разбор")}\n\n🙌Если Вы {markdown.hbold("готовы найти правильный путь в своей жизни")}, то напишите {markdown.hbold("дату рождения мне в личные сообщения — @your_mentoor👈")}'
#         kb = types.InlineKeyboardMarkup()
#         kb.add(types.InlineKeyboardButton("Получить разбор🔱", url="https://t.me/soul_mento"))

#         users_for_autosending_1 = await db_sendings.get_users_72h_autosending()
#         for user in users_for_autosending_1:
#             try:
#                 await bot.send_message(user, text, parse_mode='html', reply_markup=kb)
#                 logger.info(f'ID: {user}. Got autosending_text_72h')
#                 await db_sendings.mark_got_72h_autosending(user)
#                 await asyncio.sleep(0.2)
#             except (exceptions.BotBlocked, exceptions.UserDeactivated):
#                 logger.exception(f'ID: {user}. DELETED')
#                 await db.delete_user(user)
#             except Exception as ex:
#                 logger.error(f'got error: {ex}')

# async def on_startup(_):
#     asyncio.create_task(sending_messages_2h())
#     #asyncio.create_task(sending_message_24_h())

try:
    executor.start_polling(dp)
finally:
    stop = True
    logger.info("Бот закончил работу")

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from tgbot.keyboards.default.main_menu import m_menu, admin_menu, r_menu, manager_menu
from tgbot.states.users import Member, Admin


async def ru_language(message):
    db = message.bot.get("db")
    user_in_db = await db.select_user(telegram_id=int(message.from_user.id))
    if user_in_db.get("language") == "ru":
        return True


async def suitable_menu(message):
    db = message.bot.get("db")
    admins_list = []
    managers_list = []
    for id, telegram_id, name, password, level, regions in await db.select_all_admins():
        if level == 1:
            admins_list.append(telegram_id)
        else:
            managers_list.append(telegram_id)
    if message.from_user.id in admins_list:
        menu = admin_menu
    elif message.from_user.id in managers_list:
        menu = manager_menu
    else:
        try:
            user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
            user_in_db.get("full_name")
            menu = m_menu
        except:
            menu = r_menu

    return menu


async def bot_start(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await state.reset_state()
    try:
        user_in_db = await db.select_user(telegram_id=int(message.from_user.id))
        user_in_db.get("telegram_id")
    except:
        await db.add_user(full_name=message.from_user.full_name, telegram_id=int(message.from_user.id))

    menu = await suitable_menu(message)
    try:
        user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
        full_name = user_in_db.get("full_name")
        await message.answer(f"<b>{full_name}</b>, выберите что вас интересует:", reply_markup=menu)
    except AttributeError:
        try:
            admin_in_db = await db.select_admin(telegram_id=int(message.from_user.id))
            full_name = admin_in_db.get("name")
            if full_name is not None:
                await message.answer(f"<b>{full_name}</b>, выберите что вас интересует:", reply_markup=menu)
            else:
                await message.answer(f"Введите Ваше ФИО:")
                await Admin.Login.set()
        except AttributeError:
            full_name = message.from_user.full_name
            await message.answer(f"<b>{full_name}</b>, выберите что вас интересует:", reply_markup=menu)
            textwrap = "e:\Programming\server_keys\zommer_server2.pem"


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state="*")
    dp.register_message_handler(bot_start, text="Главное меню")
    dp.register_message_handler(bot_start, state="*", text="Главное меню")

import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.admins.custom_admins import admin_custom
from tgbot.handlers.users.start import suitable_menu
from tgbot.keyboards.default.main_menu import m_menu
from tgbot.states.users import Admin


# Admin.Login
async def login_name(message: types.Message, state: FSMContext):
    if " " in str(message.text):
        await state.update_data(name=message.text)
        await message.answer("Придумайте и введите пароль")
        await Admin.Password.set()
        await state.update_data(full_name=message.text)
    else:
        await message.answer("Введите Ваше ФИО")
        await Admin.Login.set()


# Admin.Password
async def login_password(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    name = data.get("name")
    password = message.text
    await db.update_admin(telegram_id=message.from_user.id, name=name)
    await db.update_admin(telegram_id=message.from_user.id, password=password)
    menu = await suitable_menu(message)
    await message.answer("Вы были успешно зарегестрированы", reply_markup=menu)
    await state.reset_state()


def register_admin_login(dp: Dispatcher):
    dp.register_message_handler(login_name, state=Admin.Login)
    dp.register_message_handler(login_password, state=Admin.Password)








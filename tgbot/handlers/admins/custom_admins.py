from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin, IsAdmin1
from tgbot.states.database import News


async def custom_adm(message):
    db = message.bot.get("db")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)    
    markup.insert(KeyboardButton(text="Админы"))
    markup.insert(KeyboardButton(text="Рассылка"))
    markup.insert(KeyboardButton(text="Главное Меню"))
    return markup


async def admin_custom(message: types.Message, state: FSMContext):
    markup = await custom_adm(message)
    await state.reset_state()
    await message.answer("Что вы хотите сделать ?", reply_markup=markup)


def register_custom_admins(dp: Dispatcher):
    dp.register_message_handler(admin_custom, IsAdmin1(), text="Администрация")
    dp.register_message_handler(admin_custom, state=News.Text, text="⬅️ Назад")

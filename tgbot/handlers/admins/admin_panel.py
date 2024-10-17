from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin, IsAdmin1
from tgbot.handlers.users.start import bot_start
from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.states.database import News
from tgbot.states.users import Member


# Рассылка IsAdmin1()
# News.Photo  ⬅️ Назад
# News.Confirm2  ⬅️ Назад
async def newsletter(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Отправьте текст, который хотите разослать всем пользователям", reply_markup=markup)
    await News.Text.set()


# News.Text
# News.Confirm  ⬅️ Назад
async def newsletter_text(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(KeyboardButton(text="Пропустить"))
    markup.insert(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Отправьте фото, который хотите прикрепить к текст, если не хотите прикреплять, "
                         "то нажмите <b>Пропустить</b>", reply_markup=markup)
    await News.Photo.set()
    await state.update_data(text=message.text)


# News.Photo
async def newsletter_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    photo_id = f"{message.photo[-1].file_id}"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="✅ Да"))
    markup.add(KeyboardButton(text="⬅️ Назад"))
    await message.bot.send_photo(message.chat.id, photo_id, f"{text}")
    await message.answer("Разослать это всем пользователям?", reply_markup=markup)
    await News.Confirm.set()
    await state.update_data(photo_id=photo_id)


# News.Confirm
async def newsletter_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    text = data.get("text")
    photo_id = data.get("photo_id")
    await message.answer("Выполнено.")
    await state.reset_state()
    await bot_start(message, state)
    for id, full_name, telegram_id in await db.select_all_users():
        await message.bot.send_photo(int(telegram_id), photo_id, f"{text}")


# News.Photo
async def newsletter_no_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="✅ Да"))
    markup.add(KeyboardButton(text="⬅️ Назад"))
    await message.answer(text)
    await message.answer("Все верно?", reply_markup=markup)
    await News.Confirm2.set()


# News.Confirm2
async def newsletter_confirm2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    text = data.get("text")
    await message.answer("Выполнено.")
    await state.reset_state()
    await bot_start(message, state)
    for id, full_name, telegram_id in await db.select_all_users():
        await message.bot.send_message(int(telegram_id), text)


def register_admin_panel(dp: Dispatcher):
    dp.register_message_handler(newsletter, IsAdmin1(), text="Рассылка")
    dp.register_message_handler(newsletter, state=News.Photo, text="⬅️ Назад")
    dp.register_message_handler(newsletter, state=News.Confirm2, text="⬅️ Назад")

    dp.register_message_handler(newsletter_text, state=News.Text)
    dp.register_message_handler(newsletter_text, state=News.Confirm, text="⬅️ Назад")

    dp.register_message_handler(newsletter_photo, state=News.Photo, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(newsletter_confirm, state=News.Confirm, text="✅ Да")

    dp.register_message_handler(newsletter_no_photo, state=News.Photo, text="Пропустить")
    dp.register_message_handler(newsletter_confirm2, state=News.Confirm2, text="✅ Да")



from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="База Данных")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="☎️ Контакты"),
        ],
        [
            KeyboardButton(text="Администрация"),
        ]
    ], resize_keyboard=True)


manager_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="База Данных")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="☎️ Контакты"),
        ]
    ], resize_keyboard=True)


m_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Моя База Данных")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="☎️ Контакты"),
        ],
    ], resize_keyboard=True)

r_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зарегестрироваться как Представитель")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="☎️ Контакты"),
        ],
    ], resize_keyboard=True)


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ], resize_keyboard=True)
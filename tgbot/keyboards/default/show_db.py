from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

custom_database = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Добавить"),
            KeyboardButton(text="👀 Посмотреть")
        ],
        [
            KeyboardButton(text="Главное меню")
        ]
    ], resize_keyboard=True)


categories_database = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="База врачей"),
            KeyboardButton(text="Планировние визитов")
        ],
        [
            KeyboardButton(text="Выполнение договоренности"),
            KeyboardButton(text="Визит ")
        ],
        [
            KeyboardButton(text="Визит Напоминание"),
            KeyboardButton(text="Визит Договор")
        ],
        [
            KeyboardButton(text="Визит Реализация"),
            KeyboardButton(text="Визит Выдача")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ], resize_keyboard=True)


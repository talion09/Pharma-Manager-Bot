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


customize = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Админа")
        ],
        [
            KeyboardButton(text="Главное Меню")
        ]
    ],
    resize_keyboard=True
)


async def list_admins(message: types.Message):
    await message.answer("Что вы хотите сделать ?", reply_markup=customize)


async def add_admin(message: types.Message):
    db = message.bot.get('db')
    await message.answer("Введите айди пользователя которого хотите добавить в администраторы/менеджеры\n\n"
                         "Потенциальный админ/менеджер должен у себя в боте отправить команду /get_my_id")
    text = f"Все Админы:\n\n"
    for id, telegram_id, name, password, level, regions in await db.select_all_admins():
        text += f"{name} - {telegram_id}\n"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Отменить"))
    await message.answer(text, reply_markup=markup)
    await Admin.Add_admin.set()


# Admin.Add_admin
async def add_admin_1(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    potential_admin = message.text
    admin = message.from_user.id
    if message.text == "Отменить":
        await state.reset_state()
        await admin_custom(message)
    else:
        await state.reset_state(with_data=False)
        try:
            int(potential_admin)
            user_in_db = await db.select_user(telegram_id=int(potential_admin))
            try:
                poten = user_in_db.get("telegram_id")
                if int(potential_admin) != int(admin) and int(potential_admin) == int(poten):
                    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    markup.insert(KeyboardButton(text="Назад"))
                    markup.insert(KeyboardButton(text="Администратор"))
                    markup.insert(KeyboardButton(text="Менеджер"))
                    await message.answer("Какая должность у этого пользователя?", reply_markup=markup)
                    await Admin.Add_level.set()
                    await state.update_data(potential_admin_id=int(potential_admin))
                else:
                    await message.answer(f"<b>Вы уже являетесь админом!</b>", reply_markup=customize)
            except:
                await message.answer("<b>В базе нет такого пользователя!</b>", reply_markup=customize)
        except ValueError:
            await message.answer("<b>Пожалуйста!</b> Введите айди пользователя", reply_markup=customize)


# Admin.Add_level
async def add_level_admin(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    menu = await suitable_menu(message)
    admin_name = message.from_user.full_name
    data = await state.get_data()
    potential_admin_id = int(data.get("potential_admin_id"))
    if message.text == "Назад":
        await state.reset_state()
        await add_admin(message)
    elif message.text == "Администратор":
        await state.reset_state()
        try:
            await db.add_administrator(telegram_id=int(potential_admin_id), name=None, password=None, level=1, regions='{"1": "All"}')
            await message.answer(f"Вы добавили в админы пользователя ", reply_markup=menu)
            await state.reset_state()
            await message.bot.send_message(int(potential_admin_id), f"Вы были добавлены в админы пользователем {admin_name} \nНажмите кнопку /start, чтобы завершить регистрацию")
        except Exception as err:
            print(err)
            await message.answer("<b>Этот пользователь уже добавлен в админы!</b>", reply_markup=customize)
    elif message.text == "Менеджер":
        await state.reset_state()
        try:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Назад"))
            await message.answer("Введите регионы в столбик, за которые ответственен этот менеджер\n"
                                 "Пример: \n"
                                 "<b>Город Ташкент - Бектемирский район\n"
                                 "Ташкентская область - Алмалык</b>", reply_markup=markup)
            await Admin.Add_regions.set()
            await state.update_data(potential_admin_id=int(potential_admin_id))
        except Exception as err:
            print(err)
            await message.answer("<b>Этот пользователь уже добавлен в админы!</b>", reply_markup=customize)
    else:
        pass


# Admin.Add_regions
async def add_region_admin(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    menu = await suitable_menu(message)
    admin_name = message.from_user.full_name
    data = await state.get_data()
    potential_admin_id = int(data.get("potential_admin_id"))
    msg_text = message.text
    districts = [district.strip() for district in msg_text.split('\n') if district.strip()]
    districts_dict = {i + 1: district for i, district in enumerate(districts)}
    districts_json = json.dumps(districts_dict, ensure_ascii=False, indent=4)
    if message.text == "Назад":
        await state.reset_state()
        await add_admin(message)
    else:
        await state.reset_state()
        try:
            await db.add_administrator(telegram_id=int(potential_admin_id), name=None, password=None, level=2, regions=districts_json)
            await message.answer(f"Вы добавили в Менеджеры пользователя", reply_markup=menu)
            await state.reset_state()
            await message.bot.send_message(int(potential_admin_id), f"Вы были добавлены в менеджеры пользователем {admin_name} \nНажмите кнопку /start, чтобы завершить регистрацию")
        except Exception as err:
            print(err)
            await message.answer("<b>Этот пользователь уже добавлен в админы!</b>", reply_markup=customize)


async def get_id(message: types.Message, state: FSMContext):
    await message.answer(f"Ваш айди: {message.from_user.id}")


async def number_users(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    count_users = await db.count_users()
    await message.answer(f"Количество пользователей: {count_users}")


async def add_owner(message: types.Message):
    db = message.bot.get('db')
    await db.add_administrator(telegram_id=int(153479611), name="Мухаммад", password="12345678", level=1, regions='{"1": "All"}')
    await message.answer("Выполнено")


async def drop_owner(message: types.Message):
    db = message.bot.get('db')
    await db.drop_users()
    await db.drop_admins()
    await db.drop_members()
    await db.drop_records()
    await message.answer("Выполнено")


def register_add_admin(dp: Dispatcher):
    dp.register_message_handler(list_admins, IsAdmin(), text="Админы")
    dp.register_message_handler(add_admin, IsAdmin(), text="Добавить Админа")
    dp.register_message_handler(add_admin_1, state=Admin.Add_admin)
    dp.register_message_handler(add_level_admin, state=Admin.Add_level)
    dp.register_message_handler(add_region_admin, state=Admin.Add_regions)


    dp.register_message_handler(get_id, Command("get_my_id"))
    dp.register_message_handler(number_users, Command("all_users"), IsAdmin())
    dp.register_message_handler(add_owner, Command("add_owner"))
    dp.register_message_handler(drop_owner, Command("drop_owner"))






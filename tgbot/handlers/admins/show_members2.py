from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.filters.is_admin import IsAdmin
from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.default.show_db import custom_database, categories_database
from tgbot.keyboards.inline.catalog import inline_visits
from tgbot.states.database import Admin_show
from tgbot.states.users import Member
from collections import namedtuple
import json

Record = namedtuple('Record', [
    'id', 'state_type', 'telegram_id', 'spokesman', 'spokesman_number',
    'doctor_name', 'location', 'institution', 'speciality', 'category',
    'group_of_drugs', 'doctor_phone', 'birthday', 'period_capacity',
    'calculation', 'number_of_drugs', 'term', 'total_points'
])


async def inline_markup(message: [types.Message, types.CallbackQuery], doctor_name: str, location: str):
    db = message.bot.get("db")
    inline = InlineKeyboardMarkup(row_width=2)
    select = await db.select_records(doctor_name=doctor_name, location=location)

    for row in select:
        record = Record(*row)
        if record.state_type == "Планировние визитов":
            inline.insert(InlineKeyboardButton(text=record.state_type,
                                            callback_data=inline_visits.new(record_id=int(record.id),
                                                                            action="planning")))
        elif record.state_type == "Выполнение договоренности":
            inline.insert(InlineKeyboardButton(text=record.state_type,
                                            callback_data=inline_visits.new(record_id=int(record.id),
                                                                            action="execution")))
        elif record.state_type == "Визит Договор":
            inline.insert(InlineKeyboardButton(text=record.state_type,
                                            callback_data=inline_visits.new(record_id=int(record.id),
                                                                            action="contract")))
        elif record.state_type == "Визит Реализация":
            inline.insert(InlineKeyboardButton(text=record.state_type,
                                            callback_data=inline_visits.new(record_id=int(record.id),
                                                                            action="implementation")))
        elif record.state_type == "Визит Выдача":
            inline.insert(InlineKeyboardButton(text=record.state_type,
                                            callback_data=inline_visits.new(record_id=int(record.id), action="issue")))
        else:
            pass
    return inline


async def enter_password(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton(text="Главное меню"))
    await message.answer("Введите пароль от вашего аккаунта:", reply_markup=markup)
    await Admin_show.Password_enter.set()


# Admin_show.State_type  ⬅️ Назад
# Admin_show.Password
async def my_database(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    adminn = await db.select_admin(telegram_id=message.from_user.id)
    password = adminn.get("password")
    if password != message.text:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.row(KeyboardButton(text="Главное меню"))
        await message.answer("Пароль был введен не правильно, введите его заново:", reply_markup=markup)
        await Admin_show.Password_enter.set()
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.row(KeyboardButton(text="Главное меню"))
        await message.answer("Введите ФИО врача:", reply_markup=markup)
        await Admin_show.FIO.set()


# Admin_show.FIO
async def show_doctors(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    adminn = await db.select_admin(telegram_id=message.from_user.id)
    level = int(adminn.get("level"))
    regions = adminn.get("regions")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton(text="Главное меню"))
    if level == 1:
        select = await db.select_records(doctor_name=message.text)
        doctors = []
        for row in select:
            record = Record(*row)
            if record.doctor_name not in doctors:
                doctors.append(record.doctor_name)
                text = f"<b>{record.state_type}</b>\n\n" \
                       f"Представитель: {record.spokesman}\n" \
                       f"ФИО врача: {record.doctor_name}\n" \
                       f"Номер телефона врача: {record.doctor_phone}" \
                       f"Регион и Город: {record.location}\n" \
                       f"Лечебно-профилактическое учреждение: {record.institution}\n" \
                       f"Специальность: {record.speciality}\n" \
                       f"Категория: {record.category}\n" \
                       f"Группа препаратов: {record.group_of_drugs}\n"
                inline = await inline_markup(message, str(record.doctor_name), str(record.location))
                await message.answer(text=text, reply_markup=inline)
        if len(doctors) == 0:
            await message.answer("Врач с таким ФИО не найден", reply_markup=markup)
            await state.reset_state()
        else:
            await Admin_show.Choose_inline.set()
    else:
        doctors = []
        json_data = json.loads(regions)
        for value in json_data.values():
            select = await db.select_records(doctor_name=message.text, location=value)
            for row in select:
                record = Record(*row)
                if record.doctor_name not in doctors:
                    doctors.append(record.doctor_name)
                    text = f"<b>{record.state_type}</b>\n\n" \
                           f"Представитель: {record.spokesman}\n" \
                           f"ФИО врача: {record.doctor_name}\n" \
                           f"Номер телефона врача: {record.doctor_phone}" \
                           f"Регион и Город: {record.location}\n" \
                           f"Лечебно-профилактическое учреждение: {record.institution}\n" \
                           f"Специальность: {record.speciality}\n" \
                           f"Категория: {record.category}\n" \
                           f"Группа препаратов: {record.group_of_drugs}\n"
                    inline = await inline_markup(message, str(record.doctor_name), str(record.location))
                    await message.answer(text=text, reply_markup=inline)
        if len(doctors) == 0:
            await message.answer("Врач с таким ФИО не найден", reply_markup=markup)
            await state.reset_state()
        else:
            await Admin_show.Choose_inline.set()


# Admin_show.Choose_inline
async def chosen_inline(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    record_id = int(callback_data.get("record_id"))
    action = callback_data.get("action")
    select = await db.select_record(id=record_id)
    state_type = select.get("state_type")
    spokesman = select.get("spokesman")
    doctor_name = select.get("doctor_name")
    doctor_phone = select.get("doctor_phone")
    location = select.get("location")
    institution = select.get("institution")
    speciality = select.get("speciality")
    category = select.get("category")
    group_of_drugs = select.get("group_of_drugs")
    text = f"<b>{state_type}</b>\n\n" \
           f"Представитель: {spokesman}\n" \
           f"ФИО врача: {doctor_name}\n" \
           f"Номер телефона врача: {doctor_phone}" \
           f"Регион и Город: {location}\n" \
           f"Лечебно-профилактическое учреждение: {institution}\n" \
           f"Специальность: {speciality}\n" \
           f"Категория: {category}\n" \
           f"Группа препаратов: {group_of_drugs}\n"
    inline = InlineKeyboardMarkup(row_width=1)
    inline.insert(InlineKeyboardButton(text="Назад",
                                       callback_data=inline_visits.new(record_id=int(record_id), action="back")))
    if action == "planning":
        period_capacity = select.get("period_capacity")
        text += f"Договорённость на объёма выписки по каждой позиции за период: {period_capacity}\n"
        await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=inline)
    elif action == "execution":
        calculation = select.get("calculation")
        text += f"Калькуляция выписки препарата за период в соответствии с договорённостью: {calculation}\n"
        await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=inline)
    elif action == "contract":
        number_of_drugs = select.get("number_of_drugs")
        term = select.get("term")
        text += f"Количество препаратов: {number_of_drugs}" \
                f"Период: {term}"
        await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=inline)
    elif action == "implementation":
        number_of_drugs = select.get("number_of_drugs")
        term = select.get("term")
        text += f"Количество препаратов: {number_of_drugs}" \
                f"Период: {term}"
        await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=inline)
    elif action == "issue":
        total_points = select.get("total_points")
        text += f"Количество баллов: {total_points}"
        await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=inline)
    else:
        pass


# Admin_show.Choose_inline
async def chosen_inline_back(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    record_id = int(callback_data.get("record_id"))
    action = callback_data.get("action")
    select = await db.select_record(id=record_id)
    state_type = select.get("state_type")
    spokesman = select.get("spokesman")
    doctor_name = select.get("doctor_name")
    doctor_phone = select.get("doctor_phone")
    location = select.get("location")
    institution = select.get("institution")
    speciality = select.get("speciality")
    category = select.get("category")
    group_of_drugs = select.get("group_of_drugs")
    text = f"<b>{state_type}</b>\n\n" \
           f"Представитель: {spokesman}\n" \
           f"ФИО врача: {doctor_name}\n" \
           f"Номер телефона врача: {doctor_phone}" \
           f"Регион и Город: {location}\n" \
           f"Лечебно-профилактическое учреждение: {institution}\n" \
           f"Специальность: {speciality}\n" \
           f"Категория: {category}\n" \
           f"Группа препаратов: {group_of_drugs}\n"
    inline = await inline_markup(message=call, doctor_name=str(doctor_name), location=str(location))
    await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     reply_markup=inline)


    # text = f"<b>{state_type}</b>\n\n" \
    #        f"ФИО: {message.text}\n" \
    #        f"Регион и Город: {location}\n" \
    #        f"Лечебно-профилактическое учреждение: {institution}\n"
    # for row in select:
    #     record = Record(*row)
    #     text += f"Специальность: {record.speciality}\n" \
    #             f"Категория: {record.category}\n" \
    #             f"Группа препаратов: {record.group_of_drugs}\n"
    #     if state_type == "База врачей":
    #         text += f"Номер телефона: +{record.doctor_phone}\n" \
    #                 f"День рождения: {record.birthday}\n"
    #         await message.answer(text)
    #     elif state_type == "Планировние визитов":
    #         text += f"Договорённость на объёма выписки по каждой позиции за период: {record.period_capacity}\n"
    #         await message.answer(text)
    #     elif state_type == "Выполнение договоренности":
    #         text += f"Калькуляция выписки препарата за период в соответствии с договорённостью: {record.calculation}\n"
    #         await message.answer(text)
    #     elif state_type in ["Визит", "Визит Напоминание"]:
    #         await message.answer(text)
    #     elif state_type == "Визит Договор":
    #         text += f"Количество препаратов: {record.number_of_drugs}" \
    #                 f"Период: {record.term}"
    #         await message.answer(text)
    #     elif state_type == "Визит Реализация":
    #         text += f"Количество препаратов: {record.number_of_drugs}" \
    #                 f"Период: {record.term}"
    #         await message.answer(text)
    #     elif state_type == "Визит Выдача":
    #         text += f"Количество баллов: {record.total_points}"
    #         await message.answer(text)
    #     else:
    #         pass

def register_show_members2(dp: Dispatcher):
    dp.register_message_handler(enter_password, IsAdmin(), text="База Данных")

    dp.register_message_handler(my_database, state=Admin_show.Password_enter)

    dp.register_message_handler(show_doctors, state=Admin_show.FIO)

    dp.register_callback_query_handler(chosen_inline_back, inline_visits.filter(action="back"), state=Admin_show.Choose_inline)
    dp.register_callback_query_handler(chosen_inline, inline_visits.filter(), state=Admin_show.Choose_inline)









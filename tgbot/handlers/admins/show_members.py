from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.default.show_db import custom_database, categories_database
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
    level = int(adminn.get("level"))
    regions = adminn.get("regions")
    password = adminn.get("password")
    data = await state.get_data()
    member_telegram_id = data.get("member_telegram_id")
    if member_telegram_id is not None:
        await state.update_data(member_telegram_id=member_telegram_id)
        if level == 1:
            select = await db.select_all_records()
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            members = []
            for row in select:
                record = Record(*row)
                if record.spokesman not in members:
                    members.append(record.spokesman)
                    markup.add(KeyboardButton(text=f"{record.spokesman}"))
            markup.row(KeyboardButton(text="Главное меню"))
            await message.answer("Выберите представителя:", reply_markup=markup)
            await Admin_show.Member_id.set()
        else:
            members = []
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            json_data = json.loads(regions)
            for value in json_data.values():
                select = await db.select_records(location=value)
                for row in select:
                    record = Record(*row)
                    if record.spokesman not in members:
                        members.append(record.spokesman)
                        markup.add(KeyboardButton(text=f"{record.spokesman}"))
            markup.row(KeyboardButton(text="Главное меню"))
            await message.answer("Выберите представителя:", reply_markup=markup)
            await Admin_show.Member_id.set()
    else:
        if password != message.text:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.row(KeyboardButton(text="Главное меню"))
            await message.answer("Пароль был введен не правильно, введите его заново:", reply_markup=markup)
            await Admin_show.Password_enter.set()
        else:
            if level == 1:
                select = await db.select_all_records()
                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                members = []
                for row in select:
                    record = Record(*row)
                    if record.spokesman not in members:
                        members.append(record.spokesman)
                        markup.add(KeyboardButton(text=f"{record.spokesman}"))
                markup.row(KeyboardButton(text="Главное меню"))
                await message.answer("Выберите представителя:", reply_markup=markup)
                await Admin_show.Member_id.set()
            else:
                members = []
                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                json_data = json.loads(regions)
                for value in json_data.values():
                    select = await db.select_records(location=value)
                    for row in select:
                        record = Record(*row)
                        if record.spokesman not in members:
                            members.append(record.spokesman)
                            markup.add(KeyboardButton(text=f"{record.spokesman}"))
                markup.row(KeyboardButton(text="Главное меню"))
                await message.answer("Выберите представителя:", reply_markup=markup)
                await Admin_show.Member_id.set()


# Admin_show.Location   ⬅️ Назад
# Admin_show.Member_id
async def show_database(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    member_telegram_id = data.get("member_telegram_id")
    if member_telegram_id is not None:
        await state.update_data(member_telegram_id=member_telegram_id)
    else:
        select = await db.select_member(full_name=message.text)
        member_telegram_id = int(select.get("telegram_id"))
        await state.update_data(member_telegram_id=member_telegram_id)
    await message.answer("Выберите:", reply_markup=categories_database)
    await Admin_show.State_type.set()


# Admin_show.State_type
# Admin_show.Institution  ⬅️ Назад
async def choose_state_type(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    if state_type is not None:
        await state.update_data(state_type=state_type)
        type = state_type
    else:
        await state.update_data(state_type=message.text)
        type = message.text
    member_telegram_id = int(data.get("member_telegram_id"))
    adminn = await db.select_admin(telegram_id=message.from_user.id)
    level = int(adminn.get("level"))
    regions = adminn.get("regions")
    if level == 1:
        select = await db.select_records(state_type=type, telegram_id=member_telegram_id)
        # if type == "База врачей":
        #     names = []
        #     for row in select:
        #         record = Record(*row)
        #         if record.doctor_name not in names:
        #             names.append(record.doctor_name)
        #             text = f"<b>{type}</b>\n\n" \
        #                    f"ФИО: {record.doctor_name}\n" \
        #                    f"Регион и Город: {record.location}\n" \
        #                    f"Лечебно-профилактическое учреждение: {record.institution}\n" \
        #                    f"Специальность: {record.speciality}\n" \
        #                    f"Категория: {record.category}\n" \
        #                    f"Группа препаратов: {record.group_of_drugs}\n" \
        #                    f"Номер телефона: +{record.doctor_phone}\n" \
        #                    f"День рождения: {record.birthday}\n"
        #             await message.answer(text)
        #     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        #     markup.row(KeyboardButton(text="⬅️ Назад"))
        #     markup.row(KeyboardButton(text="Главное меню"))
        #     await message.answer("Выберите:", reply_markup=markup)
        #     await Admin_show.Location.set()
        # else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        locations = []
        for row in select:
            record = Record(*row)
            if record.location not in locations:
                locations.append(record.location)
                markup.add(KeyboardButton(text=f"{record.location}"))
        markup.row(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите регион и город:", reply_markup=markup)
        await Admin_show.Location.set()
    else:
        # if type == "База врачей":
        #     names = []
        #     json_data = json.loads(regions)
        #     for value in json_data.values():
        #         select = await db.select_records(state_type=type, telegram_id=member_telegram_id, location=value)
        #         for row in select:
        #             record = Record(*row)
        #             if record.doctor_name not in names:
        #                 names.append(record.doctor_name)
        #                 text = f"<b>{type}</b>\n\n" \
        #                        f"ФИО: {record.doctor_name}\n" \
        #                        f"Регион и Город: {record.location}\n" \
        #                        f"Лечебно-профилактическое учреждение: {record.institution}\n" \
        #                        f"Специальность: {record.speciality}\n" \
        #                        f"Категория: {record.category}\n" \
        #                        f"Группа препаратов: {record.group_of_drugs}\n" \
        #                        f"Номер телефона: +{record.doctor_phone}\n" \
        #                        f"День рождения: {record.birthday}\n"
        #                 await message.answer(text)
        #         markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        #         markup.row(KeyboardButton(text="⬅️ Назад"))
        #         markup.row(KeyboardButton(text="Главное меню"))
        #         await state.update_data(doctor_name=message.text)
        #         await message.answer("Выберите:", reply_markup=markup)
        #         await Admin_show.Location.set()
        # else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        locations = []
        json_data = json.loads(regions)
        for value in json_data.values():
            select = await db.select_records(state_type=type, telegram_id=member_telegram_id, location=value)
            for row in select:
                record = Record(*row)
                if record.location not in locations:
                    locations.append(record.location)
                    markup.add(KeyboardButton(text=f"{record.location}"))
        markup.row(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите регион и город:", reply_markup=markup)
        await Admin_show.Location.set()


# Admin_show.Location
# Admin_show.Speciality  ⬅️ Назад
async def choose_location(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    member_telegram_id = int(data.get("member_telegram_id"))
    location = data.get("location")
    if location is not None:
        await state.update_data(location=location)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location)
    else:
        await state.update_data(location=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=message.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    institutions = []
    for row in select:
        record = Record(*row)
        if record.institution not in institutions:
            institutions.append(record.institution)
            markup.add(KeyboardButton(text=f"{record.institution}"))
    markup.row(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Выберите лечебно-профилактическое учреждение:", reply_markup=markup)
    await Admin_show.Institution.set()


# Admin_show.Institution
# Admin_show.Category  ⬅️ Назад
async def choose_institution(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    member_telegram_id = int(data.get("member_telegram_id"))
    location = data.get("location")
    institution = data.get("institution")
    if institution is not None:
        await state.update_data(institution=institution)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution)
    else:
        await state.update_data(institution=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=message.text)

    text = f"<b>{state_type}</b>\n\n" \
           f"ФИО: {message.text}\n" \
           f"Регион и Город: {location}\n" \
           f"Лечебно-профилактическое учреждение: {institution}\n"
    for row in select:
        record = Record(*row)
        text += f"Специальность: {record.speciality}\n" \
                f"Категория: {record.category}\n" \
                f"Группа препаратов: {record.group_of_drugs}\n"
        if state_type == "База врачей":
            text += f"Номер телефона: +{record.doctor_phone}\n" \
                    f"День рождения: {record.birthday}\n"
            await message.answer(text)
        elif state_type == "Планировние визитов":
            text += f"Договорённость на объёма выписки по каждой позиции за период: {record.period_capacity}\n"
            await message.answer(text)
        elif state_type == "Выполнение договоренности":
            text += f"Калькуляция выписки препарата за период в соответствии с договорённостью: {record.calculation}\n"
            await message.answer(text)
        elif state_type in ["Визит", "Визит Напоминание"]:
            await message.answer(text)
        elif state_type == "Визит Договор":
            text += f"Количество препаратов: {record.number_of_drugs}" \
                    f"Период: {record.term}"
            await message.answer(text)
        elif state_type == "Визит Реализация":
            text += f"Количество препаратов: {record.number_of_drugs}" \
                    f"Период: {record.term}"
            await message.answer(text)
        elif state_type == "Визит Выдача":
            text += f"Количество баллов: {record.total_points}"
            await message.answer(text)
        else:
            pass

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton(text="⬅️ Назад"))
    markup.row(KeyboardButton(text="Главное меню"))
    await state.update_data(doctor_name=message.text)
    await message.answer("Выберите:", reply_markup=markup)
    await Admin_show.Speciality.set()

    # markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # specialities = []
    # for row in select:
    #     record = Record(*row)
    #     if record.speciality not in specialities:
    #         specialities.append(record.speciality)
    #         markup.add(KeyboardButton(text=f"{record.speciality}"))
    # markup.row(KeyboardButton(text="⬅️ Назад"))
    # await message.answer("Выберите специальность врача:", reply_markup=markup)
    # await Admin_show.Speciality.set()


# Admin_show.Speciality
# Admin_show.Group_of_drugs  ⬅️ Назад
async def choose_speciality(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    member_telegram_id = int(data.get("member_telegram_id"))
    location = data.get("location")
    institution = data.get("institution")
    speciality = data.get("speciality")
    if speciality is not None:
        await state.update_data(speciality=speciality)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution, speciality=speciality)
    else:
        await state.update_data(speciality=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution, speciality=message.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories = []
    for row in select:
        record = Record(*row)
        if record.category not in categories:
            categories.append(record.category)
            markup.add(KeyboardButton(text=f"{record.category}"))
    markup.row(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Выберите категорию врача:", reply_markup=markup)
    await Admin_show.Category.set()


# Admin_show.Category
# Admin_show.Doctor_Name  ⬅️ Назад
async def choose_category(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    member_telegram_id = int(data.get("member_telegram_id"))
    location = data.get("location")
    institution = data.get("institution")
    speciality = data.get("speciality")
    category = data.get("category")
    if category is not None:
        await state.update_data(category=category)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution, speciality=speciality, category=category)
    else:
        await state.update_data(category=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution, speciality=speciality, category=message.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    group_of_drugs_list = []
    for row in select:
        record = Record(*row)
        if record.group_of_drugs not in group_of_drugs_list:
            group_of_drugs_list.append(record.group_of_drugs)
            markup.add(KeyboardButton(text=f"{record.group_of_drugs}"))
    markup.row(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Выберите группу препаратов:", reply_markup=markup)
    await Admin_show.Group_of_drugs.set()


# Admin_show.Group_of_drugs
# Admin_show.Back ⬅️ Назад
async def choose_group_of_drugs(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    member_telegram_id = int(data.get("member_telegram_id"))
    location = data.get("location")
    institution = data.get("institution")
    speciality = data.get("speciality")
    category = data.get("category")
    group_of_drugs = data.get("group_of_drugs")

    if group_of_drugs is not None:
        await state.update_data(group_of_drugs=group_of_drugs)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution, speciality=speciality, category=category, group_of_drugs=group_of_drugs)
    else:
        await state.update_data(group_of_drugs=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=member_telegram_id, location=location, institution=institution, speciality=speciality, category=category, group_of_drugs=message.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    doctor_names = []
    for row in select:
        record = Record(*row)
        if record.doctor_name not in doctor_names:
            doctor_names.append(record.doctor_name)
            markup.add(KeyboardButton(text=f"{record.doctor_name}"))
    markup.row(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Выберите врача:", reply_markup=markup)
    await Admin_show.Doctor_Name.set()


# Admin_show.Doctor_Name
async def choose_doctor_name(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    member_telegram_id = int(data.get("member_telegram_id"))
    state_type = data.get("state_type")
    location = data.get("location")
    institution = data.get("institution")
    speciality = data.get("speciality")
    category = data.get("category")
    group_of_drugs = data.get("group_of_drugs")
    text = f"<b>{state_type}</b>" \
           f"ФИО: {message.text}\n" \
           f"Регион и Город: {location}\n" \
           f"Лечебно-профилактическое учреждение: {institution}\n" \
           f"Специальность: {speciality}\n" \
           f"Категория: {category}\n" \
           f"Группа препаратов: {group_of_drugs}\n"
    select = await db.select_record(state_type=state_type, telegram_id=member_telegram_id,
                                     location=location, institution=institution, speciality=speciality,
                                     category=category, group_of_drugs=group_of_drugs, doctor_name=message.text)
    selects = await db.select_records(state_type=state_type, telegram_id=member_telegram_id,
                                      location=location, institution=institution, speciality=speciality,
                                      category=category, group_of_drugs=group_of_drugs, doctor_name=message.text)
    if state_type == "База врачей":
        doctor_phone = select.get("doctor_phone")
        doctor_birthday = select.get("birthday")
        text += f"Номер телефона: +{doctor_phone}\n" \
                f"День рождения: {doctor_birthday}\n"
        await message.answer(text)

    else:
        for row in selects:
            record = Record(*row)
            if state_type == "Планировние визитов":
                text += f"Договорённость на объёма выписки по каждой позиции за период: {record.period_capacity}\n"
                await message.answer(text)
            elif state_type == "Выполнение договоренности":
                text += f"Калькуляция выписки препарата за период в соответствии с договорённостью: {record.calculation}\n"
                await message.answer(text)
            elif state_type in ["Визит", "Визит Напоминание"]:
                await message.answer(text)
            elif state_type == "Визит Договор":
                text += f"Количество препаратов: {record.number_of_drugs}" \
                        f"Период: {record.term}"
                await message.answer(text)
            elif state_type == "Визит Реализация":
                text += f"Количество препаратов: {record.number_of_drugs}" \
                        f"Период: {record.term}"
                await message.answer(text)
            elif state_type == "Визит Выдача":
                text += f"Количество баллов: {record.total_points}"
                await message.answer(text)
            else:
                pass
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton(text="⬅️ Назад"))
    markup.row(KeyboardButton(text="Главное меню"))
    await state.update_data(doctor_name=message.text)
    await message.answer("Выберите:", reply_markup=markup)
    await Admin_show.Back.set()


def register_show_members(dp: Dispatcher):
    dp.register_message_handler(enter_password, IsAdmin(), text="База Данных")

    dp.register_message_handler(my_database, state=Admin_show.State_type, text="⬅️ Назад")
    dp.register_message_handler(my_database, state=Admin_show.Password_enter)

    dp.register_message_handler(show_database, state=Admin_show.Location, text="⬅️ Назад")
    dp.register_message_handler(show_database, state=Admin_show.Member_id)

    dp.register_message_handler(choose_state_type, state=Admin_show.Institution, text="⬅️ Назад")
    dp.register_message_handler(choose_state_type, state=Admin_show.State_type)

    dp.register_message_handler(choose_location, state=Admin_show.Speciality, text="⬅️ Назад")
    dp.register_message_handler(choose_location, state=Admin_show.Location)

    # dp.register_message_handler(choose_institution, state=Admin_show.Category, text="⬅️ Назад")
    dp.register_message_handler(choose_institution, state=Admin_show.Institution)

    # dp.register_message_handler(choose_speciality, state=Admin_show.Group_of_drugs, text="⬅️ Назад")
    # dp.register_message_handler(choose_speciality, state=Admin_show.Speciality)
    #
    # dp.register_message_handler(choose_category, state=Admin_show.Doctor_Name, text="⬅️ Назад")
    # dp.register_message_handler(choose_category, state=Admin_show.Category)
    #
    # dp.register_message_handler(choose_group_of_drugs, state=Admin_show.Back, text="⬅️ Назад")
    # dp.register_message_handler(choose_group_of_drugs, state=Admin_show.Group_of_drugs)
    #
    # dp.register_message_handler(choose_doctor_name, state=Admin_show.Doctor_Name)







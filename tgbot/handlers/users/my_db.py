from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.default.show_db import custom_database, categories_database
from tgbot.states.database import Show, Doctor
from tgbot.states.users import Member
from collections import namedtuple

# Определение namedtuple
Record = namedtuple('Record', [
    'id', 'state_type', 'telegram_id', 'spokesman', 'spokesman_number',
    'doctor_name', 'location', 'institution', 'speciality', 'category',
    'group_of_drugs', 'doctor_phone', 'birthday', 'period_capacity',
    'calculation', 'number_of_drugs', 'term', 'total_points'
])


# Show.State_type  ⬅️ Назад
# Doctor.State_type  ⬅️ Назад
async def my_database(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await state.reset_state()
    await message.answer("Выберите:", reply_markup=custom_database)


# Show.Location   ⬅️ Назад
async def show_database(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await message.answer("Выберите:", reply_markup=categories_database)
    await Show.State_type.set()


# Show.State_type
# Show.Institution  ⬅️ Назад
async def choose_state_type(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    if state_type is not None:
        typpe = state_type
        await state.update_data(state_type=state_type)
        select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id)
    else:
        typpe = message.text
        await state.update_data(state_type=message.text)
        select = await db.select_records(state_type=message.text, telegram_id=message.from_user.id)

    if len(select) == 0:
        await message.answer(f"<b>{message.text}</b> пуста, выберите:", reply_markup=categories_database)
        await Show.State_type.set()
    else:
        # if typpe == "База врачей":
        #     names = []
        #     for row in select:
        #         record = Record(*row)
        #         if record.doctor_name not in names:
        #             names.append(record.doctor_name)
        #             text = f"<b>{typpe}</b>\n\n" \
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
        #     await Show.Location.set()
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
        await Show.Location.set()


# Show.Location
# Show.Speciality  ⬅️ Назад
async def choose_location(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    location = data.get("location")
    if location is not None:
        await state.update_data(location=location)
        select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location)
    else:
        await state.update_data(location=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=message.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    institutions = []
    for row in select:
        record = Record(*row)
        if record.institution not in institutions:
            institutions.append(record.institution)
            markup.add(KeyboardButton(text=f"{record.institution}"))
    markup.row(KeyboardButton(text="⬅️ Назад"))
    await message.answer("Выберите лечебно-профилактическое учреждение:", reply_markup=markup)
    await Show.Institution.set()


# Show.Institution
# Show.Category  ⬅️ Назад
async def choose_institution(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    state_type = data.get("state_type")
    location = data.get("location")
    institution = data.get("institution")
    if institution is not None:
        await state.update_data(institution=institution)
        select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution)
    else:
        await state.update_data(institution=message.text)
        select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=message.text)

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
    await Show.Speciality.set()

    # markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # specialities = []
    # for row in select:
    #     record = Record(*row)
    #     if record.speciality not in specialities:
    #         specialities.append(record.speciality)
    #         markup.add(KeyboardButton(text=f"{record.speciality}"))
    # markup.row(KeyboardButton(text="⬅️ Назад"))
    # await message.answer("Выберите специальность врача:", reply_markup=markup)
    # await Show.Speciality.set()

#
# # Show.Speciality
# # Show.Group_of_drugs  ⬅️ Назад
# async def choose_speciality(message: types.Message, state: FSMContext):
#     db = message.bot.get("db")
#     data = await state.get_data()
#     state_type = data.get("state_type")
#     location = data.get("location")
#     institution = data.get("institution")
#     speciality = data.get("speciality")
#     if speciality is not None:
#         await state.update_data(speciality=speciality)
#         select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution, speciality=speciality)
#     else:
#         await state.update_data(speciality=message.text)
#         select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution, speciality=message.text)
#
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     categories = []
#     for row in select:
#         record = Record(*row)
#         if record.category not in categories:
#             categories.append(record.category)
#             markup.add(KeyboardButton(text=f"{record.category}"))
#     markup.row(KeyboardButton(text="⬅️ Назад"))
#     await message.answer("Выберите категорию врача:", reply_markup=markup)
#     await Show.Category.set()
#
#
# # Show.Category
# # Show.Doctor_Name  ⬅️ Назад
# async def choose_category(message: types.Message, state: FSMContext):
#     db = message.bot.get("db")
#     data = await state.get_data()
#     state_type = data.get("state_type")
#     location = data.get("location")
#     institution = data.get("institution")
#     speciality = data.get("speciality")
#     category = data.get("category")
#     if category is not None:
#         await state.update_data(category=category)
#         select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution, speciality=speciality, category=category)
#     else:
#         await state.update_data(category=message.text)
#         select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution, speciality=speciality, category=message.text)
#
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     group_of_drugs_list = []
#     for row in select:
#         record = Record(*row)
#         if record.group_of_drugs not in group_of_drugs_list:
#             group_of_drugs_list.append(record.group_of_drugs)
#             markup.add(KeyboardButton(text=f"{record.group_of_drugs}"))
#     markup.row(KeyboardButton(text="⬅️ Назад"))
#     await message.answer("Выберите группу препаратов:", reply_markup=markup)
#     await Show.Group_of_drugs.set()
#
#
# # Show.Group_of_drugs
# # Show.Back ⬅️ Назад
# async def choose_group_of_drugs(message: types.Message, state: FSMContext):
#     db = message.bot.get("db")
#     data = await state.get_data()
#     state_type = data.get("state_type")
#     location = data.get("location")
#     institution = data.get("institution")
#     speciality = data.get("speciality")
#     category = data.get("category")
#     group_of_drugs = data.get("group_of_drugs")
#
#     if group_of_drugs is not None:
#         await state.update_data(group_of_drugs=group_of_drugs)
#         select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution, speciality=speciality, category=category, group_of_drugs=group_of_drugs)
#     else:
#         await state.update_data(group_of_drugs=message.text)
#         select = await db.select_records(state_type=state_type, telegram_id=message.from_user.id, location=location, institution=institution, speciality=speciality, category=category, group_of_drugs=message.text)
#
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     doctor_names = []
#     for row in select:
#         record = Record(*row)
#         if record.doctor_name not in doctor_names:
#             doctor_names.append(record.doctor_name)
#             markup.add(KeyboardButton(text=f"{record.doctor_name}"))
#     markup.row(KeyboardButton(text="⬅️ Назад"))
#     await message.answer("Выберите врача:", reply_markup=markup)
#     await Show.Doctor_Name.set()
#
#
# # Show.Doctor_Name
# async def choose_doctor_name(message: types.Message, state: FSMContext):
#     db = message.bot.get("db")
#     data = await state.get_data()
#     state_type = data.get("state_type")
#     location = data.get("location")
#     institution = data.get("institution")
#     speciality = data.get("speciality")
#     category = data.get("category")
#     group_of_drugs = data.get("group_of_drugs")
#     text = f"<b>{state_type}</b>\n\n" \
#            f"ФИО: {message.text}\n" \
#            f"Регион и Город: {location}\n" \
#            f"Лечебно-профилактическое учреждение: {institution}\n" \
#            f"Специальность: {speciality}\n" \
#            f"Категория: {category}\n" \
#            f"Группа препаратов: {group_of_drugs}\n"
#     print(text)
#     select = await db.select_record(state_type=state_type, telegram_id=message.from_user.id,
#                                      location=location, institution=institution, speciality=speciality,
#                                      category=category, group_of_drugs=group_of_drugs, doctor_name=message.text)
#     selects = await db.select_records(state_type=state_type, telegram_id=message.from_user.id,
#                                       location=location, institution=institution, speciality=speciality,
#                                       category=category, group_of_drugs=group_of_drugs, doctor_name=message.text)
#     if state_type == "База врачей":
#         doctor_phone = select.get("doctor_phone")
#         doctor_birthday = select.get("birthday")
#         text += f"Номер телефона: +{doctor_phone}\n" \
#                 f"День рождения: {doctor_birthday}\n"
#         await message.answer(text)
#     else:
#         for row in selects:
#             record = Record(*row)
#             if state_type == "Планировние визитов":
#                 text += f"Договорённость на объёма выписки по каждой позиции за период: {record.period_capacity}\n"
#                 await message.answer(text)
#             elif state_type == "Выполнение договоренности":
#                 text += f"Калькуляция выписки препарата за период в соответствии с договорённостью: {record.calculation}\n"
#                 await message.answer(text)
#             elif state_type in ["Визит", "Визит Напоминание"]:
#                 await message.answer(text)
#             elif state_type == "Визит Договор":
#                 text += f"Количество препаратов: {record.number_of_drugs}" \
#                         f"Период: {record.term}"
#                 await message.answer(text)
#             elif state_type == "Визит Реализация":
#                 text += f"Количество препаратов: {record.number_of_drugs}" \
#                         f"Период: {record.term}"
#                 await message.answer(text)
#             elif state_type == "Визит Выдача":
#                 text += f"Количество баллов: {record.total_points}"
#                 await message.answer(text)
#             else:
#                 pass
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     markup.row(KeyboardButton(text="⬅️ Назад"))
#     markup.row(KeyboardButton(text="Главное меню"))
#     await state.update_data(doctor_name=message.text)
#     await message.answer("Выберите:", reply_markup=markup)
#     await Show.Back.set()


def register_my_db(dp: Dispatcher):
    dp.register_message_handler(my_database, state=Doctor.State_type, text="⬅️ Назад")
    dp.register_message_handler(my_database, state=Show.State_type, text="⬅️ Назад")
    dp.register_message_handler(my_database, text="Моя База Данных")

    dp.register_message_handler(show_database, state=Show.Location, text="⬅️ Назад")
    dp.register_message_handler(show_database, text="👀 Посмотреть")

    dp.register_message_handler(choose_state_type, state=Show.Institution, text="⬅️ Назад")
    dp.register_message_handler(choose_state_type, state=Show.State_type)

    dp.register_message_handler(choose_location, state=Show.Speciality, text="⬅️ Назад")
    dp.register_message_handler(choose_location, state=Show.Location)

    # dp.register_message_handler(choose_institution, state=Show.Category, text="⬅️ Назад")
    dp.register_message_handler(choose_institution, state=Show.Institution)

    # dp.register_message_handler(choose_speciality, state=Show.Group_of_drugs, text="⬅️ Назад")
    # dp.register_message_handler(choose_speciality, state=Show.Speciality)
    #
    # dp.register_message_handler(choose_category, state=Show.Doctor_Name, text="⬅️ Назад")
    # dp.register_message_handler(choose_category, state=Show.Category)
    #
    # dp.register_message_handler(choose_group_of_drugs, state=Show.Back, text="⬅️ Назад")
    # dp.register_message_handler(choose_group_of_drugs, state=Show.Group_of_drugs)
    #
    # dp.register_message_handler(choose_doctor_name, state=Show.Doctor_Name)







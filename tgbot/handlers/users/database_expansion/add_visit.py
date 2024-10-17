from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.users.my_db import my_database
from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.default.show_db import custom_database, categories_database
from tgbot.states.database import Visit, Doctor
from tgbot.states.users import Member


async def add_visitt(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    await message.answer("Введите ФИО Врача", reply_markup=cancel)
    await Visit.Doctor_Name.set()
    await state.update_data(type=type)


# Visit.Doctor_Name
async def add_doctor_name(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await state.reset_state()
        await message.answer("Выберите, что хотите добавить в базу данных:", reply_markup=categories_database)
        await Doctor.State_type.set()
    else:
        await state.update_data(doctor_name=message.text)
        await message.answer("Введите регион и город", reply_markup=cancel)
        await Visit.Location.set()


# Visit.Location
async def add_doctor_location(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите ФИО Врача", reply_markup=cancel)
        await Visit.Doctor_Name.set()
    else:
        await state.update_data(doctor_location=message.text)
        await message.answer("Введите лечебно-профилактическое учреждение", reply_markup=cancel)
        await Visit.Institution.set()


# Visit.Institution
async def add_doctor_institution(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите регион и город", reply_markup=cancel)
        await Visit.Location.set()
    else:
        await state.update_data(doctor_institution=message.text)
        await message.answer("Введите специальность врача", reply_markup=cancel)
        await Visit.Speciality.set()


# Visit.Speciality
async def add_doctor_speciality(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите лечебно-профилактическое учреждение", reply_markup=cancel)
        await Visit.Institution.set()
    else:
        await state.update_data(doctor_speciality=message.text)
        await message.answer("Введите категорию врача", reply_markup=cancel)
        await Visit.Category.set()


# Visit.Category
async def add_doctor_category(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите специальность врача", reply_markup=cancel)
        await Visit.Speciality.set()
    else:
        await state.update_data(doctor_category=message.text)
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Visit.Group_of_drugs.set()


# Visit.Group_of_drugs
async def add_doctor_group_of_drugs(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    # doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите категорию врача", reply_markup=cancel)
        await Visit.Category.set()
    else:
        if type in ["Визит", "Визит Напоминание"]:
            text = f"ФИО: {doctor_name}\n" \
                   f"Регион и Город: {doctor_location}\n" \
                   f"Лечебно-профилактическое учреждение: {doctor_institution}\n" \
                   f"Специальность: {doctor_speciality}\n" \
                   f"Категория: {doctor_category}\n" \
                   f"Группа препаратов: {message.text}\n"
            await state.update_data(doctor_group_of_drugs=message.text)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton(text="✅ Верно"))
            markup.add(KeyboardButton(text="⬅️ Назад"))
            await message.answer(text)
            await message.answer("Все верно?", reply_markup=markup)
            await Visit.Confirm.set()
        elif "Визит Договор" in type:
            await state.update_data(doctor_group_of_drugs=message.text)
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for i in range(1, 101, 10):
                start = i
                end = i + 9
                markup.add(KeyboardButton(text=f"{start}-{end}"))
            markup.row(KeyboardButton(text="⬅️ Назад"))
            await message.answer("Выберите количество препаратов на выписку за определённый период", reply_markup=markup)
            await Visit.Number_of_drugs.set()
        elif "Визит Реализация" in type:
            await state.update_data(doctor_group_of_drugs=message.text)
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for i in range(1, 101, 10):
                start = i
                end = i + 9
                markup.add(KeyboardButton(text=f"{start}-{end}"))
            markup.row(KeyboardButton(text="⬅️ Назад"))
            await message.answer("Выберите количество препаратов на отработку за определённый период", reply_markup=markup)
            await Visit.Number_of_drugs.set()
        else:
            await state.update_data(doctor_group_of_drugs=message.text)
            await message.answer("Введите сумму выданных баллов", reply_markup=cancel)
            await Visit.Total_points.set()


# ____________________________________________________________________________________________________________
# Visit.Number_of_drugs
async def add_doctor_number_of_drugs(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Visit.Group_of_drugs.set()
    else:
        await state.update_data(number_of_drugs=message.text)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for i in range(1, 12):
            markup.add(KeyboardButton(text=f"{i} месяц(а)(ев)"))
        markup.row(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите период отработки", reply_markup=markup)
        await Visit.Term.set()


# Visit.Term
async def add_doctor_term(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    number_of_drugs = data.get("doctor_group_of_drugs")
    # term = data.get("term")
    if "⬅️ Назад" in message.text:
        if "Визит Договор" in type:
            txt = "Выберите количество препаратов на выписку за определённый период"
        else:
            txt = "Выберите количество препаратов на отработку за определённый период"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for i in range(1, 101, 10):
            start = i
            end = i + 9
            markup.add(KeyboardButton(text=f"{start}-{end}"))
        markup.row(KeyboardButton(text="⬅️ Назад"))
        await message.answer(txt, reply_markup=markup)
        await Visit.Number_of_drugs.set()
    else:
        text = f"ФИО: {doctor_name}\n" \
               f"Регион и Город: {doctor_location}\n" \
               f"Лечебно-профилактическое учреждение: {doctor_institution}\n" \
               f"Специальность: {doctor_speciality}\n" \
               f"Категория: {doctor_category}\n" \
               f"Группа препаратов: {doctor_group_of_drugs}\n" \
               f"Количество препаратов: {number_of_drugs}" \
               f"Период: {message.text}"
        await state.update_data(term=message.text)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(text="✅ Верно"))
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await message.answer(text)
        await message.answer("Все верно?", reply_markup=markup)
        await Visit.Confirm3.set()


# Visit.Confirm3
async def add_doctor_confirm3(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    number_of_drugs = data.get("doctor_group_of_drugs")
    term = data.get("term")
    user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
    full_name = user_in_db.get("full_name")
    number = user_in_db.get("number")
    if "⬅️ Назад" in message.text:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for i in range(1, 12):
            markup.add(KeyboardButton(text=f"{i} месяц(а)(ев)"))
        markup.row(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите период отработки", reply_markup=markup)
        await Visit.Term.set()
    else:
        await db.add_record(state_type=type, telegram_id=message.from_user.id, spokesman=full_name,
                            spokesman_number=number, doctor_name=doctor_name, location=doctor_location,
                            institution=doctor_institution, speciality=doctor_speciality, category=doctor_category,
                            group_of_drugs=doctor_group_of_drugs, doctor_phone=None, birthday=None,
                            period_capacity=None, calculation=None, number_of_drugs=int(number_of_drugs),
                            term=term, total_points=None)
        await message.answer(f"{type} успешно занесен в Базу Данных")
        await state.reset_state()
        await my_database(message, state)


# ________________________________________________________________________________________________________
# Visit.Total_points
async def add_doctor_total_points(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Visit.Group_of_drugs.set()
    else:
        try:
            points = int(message.text)
            text = f"ФИО: {doctor_name}\n" \
                   f"Регион и Город: {doctor_location}\n" \
                   f"Лечебно-профилактическое учреждение: {doctor_institution}\n" \
                   f"Специальность: {doctor_speciality}\n" \
                   f"Категория: {doctor_category}\n" \
                   f"Группа препаратов: {doctor_group_of_drugs}\n" \
                   f"Количество баллов: {points}"
            await state.update_data(total_points=points)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton(text="✅ Верно"))
            markup.add(KeyboardButton(text="⬅️ Назад"))
            await message.answer(text)
            await message.answer("Все верно?", reply_markup=markup)
            await Visit.Confirm.set()
        except:
            await message.answer("Введите сумму выданных баллов", reply_markup=cancel)
            await Visit.Confirm2.set()


# Visit.Confirm2
async def add_doctor_confirm2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    total_points = int(data.get("total_points"))
    user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
    full_name = user_in_db.get("full_name")
    number = user_in_db.get("number")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите сумму выданных баллов", reply_markup=cancel)
        await Visit.Total_points.set()
    else:
        await db.add_record(state_type=type, telegram_id=message.from_user.id, spokesman=full_name,
                            spokesman_number=number, doctor_name=doctor_name, location=doctor_location,
                            institution=doctor_institution, speciality=doctor_speciality, category=doctor_category,
                            group_of_drugs=doctor_group_of_drugs, doctor_phone=None, birthday=None,
                            period_capacity=None, calculation=None, number_of_drugs=None, term=None,
                            total_points=int(total_points))
        await message.answer(f"{type} успешно занесен в Базу Данных")
        await state.reset_state()
        await my_database(message, state)


# _________________________________________________________________________________________________________
# Visit.Confirm
async def add_doctor_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
    full_name = user_in_db.get("full_name")
    number = user_in_db.get("number")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Visit.Group_of_drugs.set()
    else:
        await db.add_record(state_type=type, telegram_id=message.from_user.id, spokesman=full_name,
                            spokesman_number=number, doctor_name=doctor_name, location=doctor_location,
                            institution=doctor_institution, speciality=doctor_speciality, category=doctor_category,
                            group_of_drugs=doctor_group_of_drugs, doctor_phone=None, birthday=None,
                            period_capacity=None, calculation=None, number_of_drugs=None, term=None, total_points=None)
        await message.answer(f"{type} успешно занесен в Базу Данных")
        await state.reset_state()
        await my_database(message, state)


def register_add_visit(dp: Dispatcher):
    dp.register_message_handler(add_visitt, state=Doctor.State_type, text=["Визит", "Визит Напоминание",
                                                                           "Визит Договор", "Визит Реализация",
                                                                           "Визит Выдача"])
    dp.register_message_handler(add_doctor_name, state=Visit.Doctor_Name)
    dp.register_message_handler(add_doctor_location, state=Visit.Location)
    dp.register_message_handler(add_doctor_institution, state=Visit.Institution)
    dp.register_message_handler(add_doctor_speciality, state=Visit.Speciality)
    dp.register_message_handler(add_doctor_category, state=Visit.Category)
    dp.register_message_handler(add_doctor_group_of_drugs, state=Visit.Group_of_drugs)
    dp.register_message_handler(add_doctor_confirm, state=Visit.Confirm)

    dp.register_message_handler(add_doctor_number_of_drugs, state=Visit.Number_of_drugs)
    dp.register_message_handler(add_doctor_term, state=Visit.Term)
    dp.register_message_handler(add_doctor_confirm3, state=Visit.Confirm3)

    dp.register_message_handler(add_doctor_total_points, state=Visit.Total_points)
    dp.register_message_handler(add_doctor_confirm2, state=Visit.Confirm2)










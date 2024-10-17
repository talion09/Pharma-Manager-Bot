from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.users.my_db import my_database
from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.default.show_db import custom_database, categories_database
from tgbot.states.database import Doctor
from tgbot.states.users import Member


async def add_database(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await message.answer("Выберите, что хотите добавить в базу данных:", reply_markup=categories_database)
    await Doctor.State_type.set()


# Doctor.State_type
async def add_doctor(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await message.answer("Введите ФИО Врача", reply_markup=cancel)
    await Doctor.Doctor_Name.set()
    await state.update_data(type=message.text)


# Doctor.Doctor_Name
async def add_doctor_name(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await state.reset_state()
        await message.answer("Выберите, что хотите добавить в базу данных:", reply_markup=categories_database)
        await Doctor.State_type.set()
    else:
        await state.update_data(doctor_name=message.text)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(KeyboardButton(text="Город Ташкент"))
        markup.add(KeyboardButton(text="Ташкентская область"))
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите город", reply_markup=markup)
        await Doctor.Location_0.set()


# Doctor.Location_0
async def add_doctor_location_0(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите ФИО Врача", reply_markup=cancel)
        await Doctor.Doctor_Name.set()
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        if message.text == "Город Ташкент":
            markup.add(KeyboardButton(text="Бектемирский район"))
            markup.add(KeyboardButton(text="Юнусабадский район"))
            markup.add(KeyboardButton(text="Учтепинский район"))
            markup.add(KeyboardButton(text="Янгихаётский район"))
            markup.add(KeyboardButton(text="Мирзо-Улугбекский район"))
            markup.add(KeyboardButton(text="Мирабадский район"))
            markup.add(KeyboardButton(text="Яккасарайский район"))
            markup.add(KeyboardButton(text="Яшнободский район"))
            markup.add(KeyboardButton(text="Чиланзарский район"))
            markup.add(KeyboardButton(text="Шайхантахурский район"))
            markup.add(KeyboardButton(text="Алмазарский район"))
            markup.add(KeyboardButton(text="Сергелийский район"))
        elif message.text == "Ташкентская область":
            markup.add(KeyboardButton(text="Букинский район"))
            markup.add(KeyboardButton(text="Алмалык"))
            markup.add(KeyboardButton(text="Ангрен"))
            markup.add(KeyboardButton(text="Чирчик"))
            markup.add(KeyboardButton(text="Зангиатинский район"))
            markup.add(KeyboardButton(text="Юкоричирчикский район"))
            markup.add(KeyboardButton(text="Кибрайский район"))
            markup.add(KeyboardButton(text="Янгиюльский район"))
            markup.add(KeyboardButton(text="Ташкентский район"))
            markup.add(KeyboardButton(text="Нурафшон"))
        else:
            pass
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await state.update_data(location_0=message.text)
        await message.answer("Выберите район", reply_markup=markup)
        await Doctor.Location.set()


# Doctor.Location
async def add_doctor_location(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(KeyboardButton(text="Город Ташкент"))
        markup.add(KeyboardButton(text="Ташкентская область"))
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите", reply_markup=markup)
        await Doctor.Location_0.set()
    else:
        data = await state.get_data()
        location_0 = data.get("location_0")
        await state.update_data(doctor_location=f"{location_0} - {message.text}")
        await message.answer("Введите лечебно-профилактическое учреждение", reply_markup=cancel)
        await Doctor.Institution.set()


# Doctor.Institution
async def add_doctor_institution(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите регион и город", reply_markup=cancel)
        await Doctor.Location.set()
    else:
        await state.update_data(doctor_institution=message.text)
        await message.answer("Введите специальность врача", reply_markup=cancel)
        await Doctor.Speciality.set()


# Doctor.Speciality
async def add_doctor_speciality(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите лечебно-профилактическое учреждение", reply_markup=cancel)
        await Doctor.Institution.set()
    else:
        await state.update_data(doctor_speciality=message.text)
        await message.answer("Введите категорию врача", reply_markup=cancel)
        await Doctor.Category.set()


# Doctor.Category
async def add_doctor_category(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите специальность врача", reply_markup=cancel)
        await Doctor.Speciality.set()
    else:
        await state.update_data(doctor_category=message.text)
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Doctor.Group_of_drugs.set()


# ____________________________________________________________________________________________________________________
# Doctor.Group_of_drugs
async def add_doctor_group_of_drugs(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите категорию врача", reply_markup=cancel)
        await Doctor.Category.set()
    else:
        if type == "База врачей":
            await state.update_data(doctor_group_of_drugs=message.text)
            await message.answer("Введите телефонный номер врача (+998xxxxxxxxx):", reply_markup=cancel)
            await Doctor.Phone.set()
        elif type == "Планировние визитов":
            await state.update_data(doctor_group_of_drugs=message.text)
            await message.answer("Введите договорённость на объёма выписки по каждой позиции за период", reply_markup=cancel)
            await Doctor.Extra.set()
        elif type == "Выполнение договоренности":
            await state.update_data(doctor_group_of_drugs=message.text)
            await message.answer("Введите калькуляцию выписки препарата за период в соответствии с договорённостью", reply_markup=cancel)
            await Doctor.Extra.set()


# Doctor.Extra
async def add_doctor_extra(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    # doctor_extra = data.get("doctor_extra")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Doctor.Group_of_drugs.set()
    else:
        text = f"ФИО: {doctor_name}\n" \
               f"Регион и Город: {doctor_location}\n" \
               f"Лечебно-профилактическое учреждение: {doctor_institution}\n" \
               f"Специальность: {doctor_speciality}\n" \
               f"Категория: {doctor_category}\n" \
               f"Группа препаратов: {doctor_group_of_drugs}\n" \
               f"Доролнительно: {message.text}"
        await state.update_data(doctor_extra=message.text)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(text="✅ Верно"))
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Все верно?", reply_markup=markup)
        await Doctor.Confirm2.set()


# Doctor.Confirm2
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
    doctor_extra = data.get("doctor_extra")
    user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
    full_name = user_in_db.get("full_name")
    number = user_in_db.get("number")
    if "⬅️ Назад" in message.text:
        if type == "Планировние визитов":
            await state.update_data(doctor_group_of_drugs=message.text)
            await message.answer("Введите Договорённость на объёма выписки по каждой позиции за период", reply_markup=cancel)
            await Doctor.Extra.set()
        elif type == "Выполнение договоренности":
            await state.update_data(doctor_group_of_drugs=message.text)
            await message.answer("Введите калькуляцию выписки препарата за период в соответствии с договорённостью", reply_markup=cancel)
            await Doctor.Extra.set()
    else:
        if type == "Планировние визитов":
            await db.add_record(state_type=type, telegram_id=message.from_user.id, spokesman=full_name,
                                spokesman_number=number, doctor_name=doctor_name, location=doctor_location,
                                institution=doctor_institution, speciality=doctor_speciality, category=doctor_category,
                                group_of_drugs=doctor_group_of_drugs, doctor_phone=None, birthday=None,
                                period_capacity=doctor_extra, calculation=None, number_of_drugs=None, term=None,
                                total_points=None)
        elif type == "Выполнение договоренности":
            await db.add_record(state_type=type, telegram_id=message.from_user.id, spokesman=full_name,
                                spokesman_number=number, doctor_name=doctor_name, location=doctor_location,
                                institution=doctor_institution, speciality=doctor_speciality, category=doctor_category,
                                group_of_drugs=doctor_group_of_drugs, doctor_phone=None, birthday=None,
                                period_capacity=None, calculation=doctor_extra, number_of_drugs=None, term=None,
                                total_points=None)

        await message.answer(f"{type} успешно занесен в Базу Данных")
        await state.reset_state()
        await my_database(message, state)


# ____________________________________________________________________________________________________________________
# Doctor.Phone
async def add_doctor_phone(message: types.Message, state: FSMContext):
    if "⬅️ Назад" in message.text:
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Doctor.Group_of_drugs.set()
    else:
        phone = message.text[1:]
        try:
            int(phone)
            if "+998" in str(message.text) and len(message.text) == 13:
                await state.update_data(doctor_phone=phone)
                await message.answer("Введите дату рождения врача", reply_markup=cancel)
                await Doctor.Birthday.set()
            else:
                await message.answer("Введите телефонный номер врача (+998xxxxxxxxx):", reply_markup=cancel)
                await Doctor.Phone.set()
        except:
            await message.answer("Введите телефонный номер врача (+998xxxxxxxxx):", reply_markup=cancel)
            await Doctor.Phone.set()


# Doctor.Birthday
async def add_doctor_birthday(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    type = data.get("type")
    doctor_name = data.get("doctor_name")
    doctor_location = data.get("doctor_location")
    doctor_institution = data.get("doctor_institution")
    doctor_speciality = data.get("doctor_speciality")
    doctor_category = data.get("doctor_category")
    doctor_group_of_drugs = data.get("doctor_group_of_drugs")
    doctor_phone = data.get("doctor_phone")
    # doctor_birthday = data.get("doctor_birthday")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите телефонный номер врача (+998xxxxxxxxx):", reply_markup=cancel)
        await Doctor.Phone.set()
    else:
        text = f"ФИО: {doctor_name}\n" \
               f"Регион и Город: {doctor_location}\n" \
               f"Лечебно-профилактическое учреждение: {doctor_institution}\n" \
               f"Специальность: {doctor_speciality}\n" \
               f"Категория: {doctor_category}\n" \
               f"Группа препаратов: {doctor_group_of_drugs}\n" \
               f"Номер телефона: +{doctor_phone}\n" \
               f"День рождения: {message.text}\n"
        await state.update_data(doctor_birthday=message.text)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(text="✅ Верно"))
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await message.answer(text)
        await message.answer("Все верно?", reply_markup=markup)
        await Doctor.Confirm.set()


# Doctor.Confirm
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
    doctor_phone = data.get("doctor_phone")
    doctor_birthday = data.get("doctor_birthday")
    user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
    full_name = user_in_db.get("full_name")
    number = user_in_db.get("number")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите дату рождения врача", reply_markup=cancel)
        await Doctor.Birthday.set()
    else:
        await db.add_record(state_type=type, telegram_id=message.from_user.id, spokesman=full_name,
                            spokesman_number=number, doctor_name=doctor_name, location=doctor_location,
                            institution=doctor_institution, speciality=doctor_speciality, category=doctor_category,
                            group_of_drugs=doctor_group_of_drugs, doctor_phone=int(doctor_phone),
                            birthday=doctor_birthday, period_capacity=None, calculation=None, number_of_drugs=None,
                            term=None, total_points=None)
        await message.answer(f"{type} успешно занесен в Базу Данных")
        await state.reset_state()
        await my_database(message, state)


def register_add_db(dp: Dispatcher):
    dp.register_message_handler(add_database, text="➕ Добавить")

    dp.register_message_handler(add_doctor, state=Doctor.State_type, text=["База врачей", "Планировние визитов", "Выполнение договоренности"])
    dp.register_message_handler(add_doctor_name, state=Doctor.Doctor_Name)
    dp.register_message_handler(add_doctor_location_0, state=Doctor.Location_0)
    dp.register_message_handler(add_doctor_location, state=Doctor.Location)
    dp.register_message_handler(add_doctor_institution, state=Doctor.Institution)
    dp.register_message_handler(add_doctor_speciality, state=Doctor.Speciality)
    dp.register_message_handler(add_doctor_category, state=Doctor.Category)
    dp.register_message_handler(add_doctor_group_of_drugs, state=Doctor.Group_of_drugs)
    dp.register_message_handler(add_doctor_phone, state=Doctor.Phone)
    dp.register_message_handler(add_doctor_birthday, state=Doctor.Birthday)
    dp.register_message_handler(add_doctor_confirm, state=Doctor.Confirm)

    dp.register_message_handler(add_doctor_extra, state=Doctor.Extra)
    dp.register_message_handler(add_doctor_confirm2, state=Doctor.Confirm2)









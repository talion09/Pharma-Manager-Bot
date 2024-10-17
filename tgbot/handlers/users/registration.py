from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.users.start import suitable_menu
from tgbot.keyboards.default.main_menu import m_menu, cancel
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.states.users import Member


# Зарегестрироваться как Представитель
async def registration(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    menu = await suitable_menu(message)
    try:
        user_in_db = await db.select_member(telegram_id=int(message.from_user.id))
        full_name = user_in_db.get("full_name")
        await message.answer(f"{full_name}, Вы уже являетесь представителем", reply_markup=menu)
    except AttributeError:
        try:
            admin_in_db = await db.select_admin(telegram_id=int(message.from_user.id))
            full_name = admin_in_db.get("name")
            await message.answer(f"{full_name}, Вы уже зарегестрированы как админ", reply_markup=menu)
        except AttributeError:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.row(KeyboardButton(text="Главное меню"))
            await message.answer(f"Здравствуйте! {message.from_user.full_name}\nВведите Ваше ФИО",
                                 reply_markup=phonenumber)
            await Member.Name.set()


# Member.Name
async def registration_name(message: types.Message, state: FSMContext):
    if " " in str(message.text):
        await state.update_data(name=message.text)
        await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
        await Member.Phone.set()
    else:
        await message.answer("Введите Ваше ФИО")
        await Member.Name.set()


# Member.Phone
async def registration_phone(message: types.Message, state: FSMContext):
    contc = message.contact.phone_number
    await state.update_data(number=contc[1:])
    await message.answer("Введите регион и город", reply_markup=cancel)
    await Member.Location.set()


# Member.Phone
async def registration_phone_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = message.text[1:]
    try:
        int(phone)
        if "+998" in str(message.text) and len(message.text) == 13:
            await state.update_data(number=phone)
            await message.answer("Введите регион и город", reply_markup=cancel)
            await Member.Location.set()
        else:
            await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
            await Member.Phone.set()
    except:
        await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
        await Member.Phone.set()


# Member.Location
async def registration_location(message: types.Message, state: FSMContext):
    if "⬅️ Назад" in message.text:
        await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
        await Member.Phone.set()
    else:
        await state.update_data(location=message.text)
        await message.answer("Введите ФИО Вашего менеджера", reply_markup=cancel)
        await Member.Memder_Manager.set()


# Member.Memder_Manager
async def registration_memder_manager(message: types.Message, state: FSMContext):
    if "⬅️ Назад" in message.text:
        await message.answer("Введите регион и город", reply_markup=cancel)
        await Member.Location.set()
    else:
        await state.update_data(memder_manager=message.text)
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Member.Group_of_drugs.set()


# Member.Group_of_drugs
async def registration_group_of_drugs(message: types.Message, state: FSMContext):
    if "⬅️ Назад" in message.text:
        await message.answer("Введите ФИО Вашего менеджера", reply_markup=cancel)
        await Member.Memder_Manager.set()
    else:
        await state.update_data(group_of_drugs=message.text)
        await message.answer("Введите дату Вашего дня рождения", reply_markup=cancel)
        await Member.Birthday.set()


# Member.Birthday
async def registration_birthday(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    number = data.get("number")
    location = data.get("location")
    memder_manager = data.get("memder_manager")
    group_of_drugs = data.get("group_of_drugs")
    # birthday = data.get("birthday")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите группу препаратов", reply_markup=cancel)
        await Member.Group_of_drugs.set()
    else:
        text = f"ФИО: {name}\n" \
               f"Номер телефона: +{number}\n" \
               f"Регион и Город: {location}\n" \
               f"Менеджер: {memder_manager}\n" \
               f"Группа препаратов: {group_of_drugs}\n" \
               f"День рождения: {message.text}\n"
        await state.update_data(birthday=message.text)
        await message.answer(text)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(text="✅ Верно"))
        markup.add(KeyboardButton(text="⬅️ Назад"))
        await message.answer("Все верно?", reply_markup=markup)
        await Member.Next.set()


# Member.Next
async def registration_next(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    name = data.get("name")
    number = int(data.get("number"))
    location = data.get("location")
    memder_manager = data.get("memder_manager")
    group_of_drugs = data.get("group_of_drugs")
    birthday = data.get("birthday")
    if "⬅️ Назад" in message.text:
        await message.answer("Введите дату Вашего дня рождения", reply_markup=cancel)
        await Member.Birthday.set()
    else:
        await db.add_member(
            telegram_id=message.from_user.id,
            full_name=name,
            number=number,
            location=location,
            memder_manager=memder_manager,
            group_of_drugs=group_of_drugs,
            birthday=birthday
        )
        await state.reset_state()
        await message.answer(f"{name}, Выберите что вас интересует:", reply_markup=m_menu)


def register_registration(dp: Dispatcher):
    dp.register_message_handler(registration, text="Зарегестрироваться как Представитель")
    dp.register_message_handler(registration_name, state=Member.Name)
    dp.register_message_handler(registration_phone_text, state=Member.Phone, content_types=types.ContentType.TEXT)
    dp.register_message_handler(registration_phone, state=Member.Phone, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(registration_location, state=Member.Location)
    dp.register_message_handler(registration_memder_manager, state=Member.Memder_Manager)
    dp.register_message_handler(registration_group_of_drugs, state=Member.Group_of_drugs)
    dp.register_message_handler(registration_birthday, state=Member.Birthday)
    dp.register_message_handler(registration_next, state=Member.Next)




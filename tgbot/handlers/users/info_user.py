# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
#
# from tgbot.keyboards.default.main_menu import m_menu_uz, m_menu
# from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
# from tgbot.states.users import User
#
#
# # User.Lang
# async def info_lang(message: types.Message, state: FSMContext):
#     if message.text == "🇷🇺 Ru":
#         language = "🇷🇺 Ru"
#         await message.answer("Введите Ваше Имя и Фамилию")
#         await state.update_data(lang=language)
#         await User.Name.set()
#     elif message.text == "🇺🇿 Uz":
#         language = "🇺🇿 Uz"
#         await message.answer("To'liq ismingizni kiriting")
#         await state.update_data(lang=language)
#         await User.Name.set()
#     else:
#         await message.answer("Выберите язык:\n\nTilni tanlang:")
#
#
# # User.Name
# async def info_name(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     language = data.get("lang")
#     if " " in str(message.text):
#         await state.update_data(name=message.text)
#         if language == "🇷🇺 Ru":
#             await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
#         else:
#             await message.answer("Telefon raqamingizni yuboring (+998xxxxxxxxx):", reply_markup=phonenumber_uz)
#         await User.Phone.set()
#     else:
#         if language == "🇷🇺 Ru":
#             await message.answer("Введите Ваше Имя и Фамилию")
#         else:
#             await message.answer("To'liq ismingizni kiriting")
#         await User.Name.set()
#
#
# # User.Phone
# async def info_phone(message: types.Message, state: FSMContext):
#     contc = message.contact.phone_number
#     await state.update_data(number=contc)
#     await User.Next.set()
#     await info_next(message, state)
#
#
# # User.Phone
# async def info_phone_text(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     language = data.get("lang")
#     phone = message.text[1:]
#     try:
#         int(phone)
#         if "+998" in str(message.text) and len(message.text) == 13:
#             await state.update_data(number=phone)
#             await User.Next.set()
#             await info_next(message, state)
#         else:
#             if language == "🇷🇺 Ru":
#                 await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
#             else:
#                 await message.answer("Telefon raqamingizni yuboring (+998xxxxxxxxx):", reply_markup=phonenumber_uz)
#             await User.Phone.set()
#     except:
#         if language == "🇷🇺 Ru":
#             await message.answer("Отправьте ваш номер телефона (+998xxxxxxxxx):", reply_markup=phonenumber)
#         else:
#             await message.answer("Telefon raqamingizni yuboring (+998xxxxxxxxx):", reply_markup=phonenumber_uz)
#         await User.Phone.set()
#
#
# # User.Next
# async def info_next(message: types.Message, state: FSMContext):
#     db = message.bot.get("db")
#     data = await state.get_data()
#     language = data.get("lang")
#     number = data.get("number")
#     name = data.get("name")
#     username = message.from_user.username
#     if language == "🇷🇺 Ru":
#         await message.answer(
#             f"{name}, Выберите что вас интересует:",
#             reply_markup=m_menu)
#         language = "ru"
#     else:
#         await message.answer(
#             f"{name}, Sizni qiziqtirgan narsani tanlang:",
#             reply_markup=m_menu_uz)
#         language = "uz"
#
#     await db.add_user(
#         full_name=name,
#         username=username,
#         telegram_id=int(message.from_user.id),
#         language=language
#     )
#
#     await state.reset_state()
#
#
# def register_info_user(dp: Dispatcher):
#     dp.register_message_handler(info_lang, state=User.Lang)
#     dp.register_message_handler(info_name, state=User.Name)
#     dp.register_message_handler(info_phone_text, state=User.Phone, content_types=types.ContentType.TEXT)
#     dp.register_message_handler(info_phone, state=User.Phone, content_types=types.ContentType.CONTACT)
#     dp.register_message_handler(info_next, state=User.Next)
#
#
#

from aiogram.types import Message
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        db = message.bot.get('db')
        admins_list = []
        for id, telegram_id, name, password, level, regions in await db.select_all_admins():
            admins_list.append(telegram_id)
        return message.from_user.id in admins_list


class IsAdmin1(BoundFilter):
    async def check(self, message: Message):
        db = message.bot.get('db')
        admins_list = []
        for id, telegram_id, name, password, level, regions in await db.select_all_admins():
            if level == 1:
                admins_list.append(telegram_id)
        return message.from_user.id in admins_list




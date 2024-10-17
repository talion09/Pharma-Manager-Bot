import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.db_api.postgresql import Database
from tgbot.config import load_config
from tgbot.filters.is_admin import IsAdmin, IsAdmin1
from tgbot.handlers.admins.add_admin import register_add_admin
from tgbot.handlers.admins.admin_login import register_admin_login
from tgbot.handlers.admins.admin_panel import register_admin_panel
from tgbot.handlers.admins.custom_admins import register_custom_admins
from tgbot.handlers.admins.show_members2 import register_show_members2
from tgbot.handlers.users.database_expansion.add_db import register_add_db
from tgbot.handlers.users.database_expansion.add_visit import register_add_visit
from tgbot.handlers.users.my_db2 import register_my_db2
from tgbot.handlers.users.registration import register_registration
from tgbot.handlers.users.start import register_start
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_filters(dp):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsAdmin1)


def register_all_handlers(dp):
    register_start(dp)

    register_custom_admins(dp)
    register_add_admin(dp)
    register_admin_login(dp)
    register_show_members2(dp)
    register_admin_panel(dp)

    register_registration(dp)
    register_my_db2(dp)
    register_add_db(dp)
    register_add_visit(dp)


async def main():
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    db = Database()

    bot['config'] = config

    register_all_filters(dp)
    register_all_handlers(dp)

    await db.create()

    # await db.drop_users()
    # await db.drop_admins()
    # await db.drop_members()
    # await db.drop_records()

    await db.create_table_users()
    await db.create_table_admins()
    await db.create_table_members()
    await db.create_table_records()


    bot['db'] = db

    await set_default_commands(dp)
    await on_startup_notify(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

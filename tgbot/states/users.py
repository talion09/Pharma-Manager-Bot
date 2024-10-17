from aiogram.dispatcher.filters.state import StatesGroup, State


class Member(StatesGroup):
    Name = State()
    Phone = State()
    Location = State()
    Memder_Manager = State()
    Group_of_drugs = State()
    Birthday = State()
    Next = State()


class Admin(StatesGroup):
    Add_admin = State()
    Add_level = State()
    Add_regions = State()
    Login = State()
    Password = State()
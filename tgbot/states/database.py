from aiogram.dispatcher.filters.state import StatesGroup, State


class Doctor(StatesGroup):
    State_type = State()
    Doctor_Name = State()
    Location_0 = State()
    Location = State()
    Institution = State()
    Speciality = State()
    Category = State()
    Group_of_drugs = State()
    Phone = State()
    Birthday = State()
    Confirm = State()

    Extra = State()
    Confirm2 = State()

    # лечебно-профилактическое учреждение


class Visit(StatesGroup):
    Doctor_Name = State()
    Location = State()
    Institution = State()
    Speciality = State()
    Category = State()
    Group_of_drugs = State()
    Confirm = State()

    Total_points = State()
    Confirm2 = State()

    Number_of_drugs = State()
    Term = State()
    Confirm3 = State()


class Show(StatesGroup):
    State_type = State()
    Location = State()
    Institution = State()
    Speciality = State()
    Category = State()
    Group_of_drugs = State()
    Doctor_Name = State()
    Back = State()

    FIO = State()
    Choose_inline = State()

class Admin_show(StatesGroup):
    Password_enter = State()
    Member_id = State()
    State_type = State()
    Location = State()
    Institution = State()
    Speciality = State()
    Category = State()
    Group_of_drugs = State()
    Doctor_Name = State()
    Back = State()

    FIO = State()
    Choose_inline = State()



class News(StatesGroup):
    Text = State()
    Photo = State()
    Confirm = State()
    Confirm2 = State()





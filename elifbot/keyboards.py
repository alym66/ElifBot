from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from sqlite_db import get_staff_names

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Посмотреть проекты').add('Добавить проект').add('Посмотреть состав').add('Добавить сотрудника')

catalog_list = ReplyKeyboardMarkup(resize_keyboard=True)
catalog_list.add('Digitals').add('Education').add('Commerce')


async def create_staff_keyboard():
    staff_names = await get_staff_names()
    staff_list = ReplyKeyboardMarkup(resize_keyboard=True)

    for staff_name in staff_names:
        staff_list.add(KeyboardButton(staff_name))
    return staff_list

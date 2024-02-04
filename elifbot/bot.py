from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import keyboards as kb
import sqlite_db as db

storage = MemoryStorage()
bot = Bot('6495293586:AAG9vnQzPfBdDgrl_wtEEi2gAQwLHoGnkmI')
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот запущен!')


class NewStaff(StatesGroup):
    full_name = State()
    about = State()


class NewOrder(StatesGroup):
    name = State()
    description = State()
    performers = State()
    department = State()
    deadline = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAMpZBAAAfUO9xqQuhom1S8wBMW98ausAAI4CwACTuSZSzKxR9LZT4zQLwQ')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в Elif!',
                         reply_markup=kb.main)


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'ID: {message.from_user.id}')


@dp.message_handler(text=['Посмотреть проекты'])
async def digital(message: types.Message):
    await message.answer('Выберите отдел', reply_markup=kb.catalog_list)


@dp.message_handler(text='Добавить сотрудника')
async def add_staff(message: types.Message):
    await message.answer('Напишите полное имя сотрудника')
    await NewStaff.full_name.set()


@dp.message_handler(state=NewStaff.full_name)
async def add_staff_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
    await message.answer('Напишите специальность сотрудника')
    await NewStaff.next()

@dp.message_handler(state=NewStaff.about)
async def add_staff_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
    await db.add_staff(state)
    await message.answer('Сотрудник успешно добавлен')
    await state.finish()


@dp.message_handler(text='Добавить проект')
async def add_project(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEDEy9lskt64G7Sv_w8s2L-CqMXLzSYJwACjxIAA8nhSYiNnF7PajHuNAQ')
    await message.answer('Напишите название проекта')
    await NewOrder.name.set()


@dp.message_handler(state=NewOrder.name)
async def add_project_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание проекта')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.description)
async def add_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    staff_kb = await kb.create_staff_keyboard()
    await message.answer('Напишите участников проекта', reply_markup=staff_kb)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.performers)
async def add_performers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['performers'] = message.text
    await message.answer('Выберите отдел проекта', reply_markup=kb.catalog_list)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.department)
async def add_performers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['department'] = message.text
    await message.answer('Напишите дедлайн проекта')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.deadline)
async def add_deadline(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deadline'] = message.text

    await db.add_project(state)
    await message.answer_sticker('CAACAgIAAxkBAAEDEydlsksquWFnPRGQuQ5spReOEC9f8wAC-Q0AAouP2UmKjqN_h99EPzQE')
    await message.answer('Проект успешно добавлен')
    await state.finish()


@dp.message_handler(text=['Digitals', 'Education', 'Commerce'])
async def show_projects(message: types.Message):
    await db.show_projects(message)

@dp.message_handler(text='Посмотреть состав')
async def show_staff(message: types.Message):
    await db.show_staff(message)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

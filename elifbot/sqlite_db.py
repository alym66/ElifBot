import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect('tg.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS staff("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "full_name TEXT,"
                "about TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS project("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT,"
                "description TEXT,"
                "performers TEXT,"
                "department TEXT,"
                "deadline TEXT)")
    db.commit()


async def add_staff(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO staff (full_name, about) VALUES (?, ?)",
                    (data['full_name'], data['about']))
        db.commit()


async def add_project(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO project (name, description, performers, department, deadline) VALUES (?, ?, ?, ?, ?)",
                    (data['name'], data['description'], data['performers'], data['department'], data['deadline']))
        db.commit()


async def show_staff(message):
    cur.execute("SELECT id, full_name, about FROM staff")
    staff = cur.fetchall()
    for member in staff:
        id, full_name, about = member
        member_info = (f'''ID сотрудника: {id}
        
Имя и фамилия: {full_name}
Область: {about}''')
        await message.answer(member_info)

    db.commit()


async def show_projects(message):
    if message.text in ['Digitals', 'Education', 'Commerce']:
        department = message.text

        cur.execute(
            f"SELECT id, name, description, performers, deadline FROM project where department = '{department}'")
        projects = cur.fetchall()

        if projects:
            for project in projects:
                id, name, description, performers, deadline = project
                project_info = (f'''ID Проекта: {id}
Название: {name}

Описание: {description}

Выполняют: {performers}
Дедлайн: {deadline}''')
                await message.answer(project_info)
        else:
            await message.answer(f"Не найдено проектов для отдела {department}.")

    db.commit()


async def get_staff_names():
    cur.execute("SELECT full_name FROM staff")
    rows = cur.fetchall()
    return [row[0] for row in rows]
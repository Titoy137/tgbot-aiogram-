import sqlite3 as sq

async def db_start_krz():

    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS mykorzin(user_id TEXT PRIMARY KEY, zakaz TEXT, kolvo INTEGER)")

    db.commit()


async def create_korzina(user_id):
    user = cur.execute("SELECT 1 FROM mykorzin WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO mykorzin VALUES(?, ?, ?)", (user_id, '', ''))
        db.commit()

async def edit_korzina(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE mykorzin SET zakaz = '{}', kolvo = '{}' WHERE user_id == '{}'".format(
            data['zakaz'], data['kolvo'], user_id))
        db.commit()

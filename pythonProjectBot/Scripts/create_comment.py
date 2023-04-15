import sqlite3 as sq

async def db_start_com():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS mypcomment(user_id TEXT PRIMARY KEY, commentariy TEXT)")

    db.commit()


async def create_comment(user_id):
    user = cur.execute("SELECT 1 FROM mypcomment WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO mypcomment VALUES(?, ?)", (user_id, ''))
        db.commit()

async def edit_comment(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE mypcomment SET commentariy = '{}' WHERE user_id == '{}'".format(
            data['commentariy'], user_id))
        db.commit()

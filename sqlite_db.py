import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('info.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, balance INTEGER)")

    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?)", (user_id, '', ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET name ='{}', balance ='{}' WHERE user_id == '{}' ".format(
            data['name'], data['balance'], user_id))
        db.commit()


async def select_balance():
        balance_check = cur.execute("SELECT * FROM profile").fetchall()

        return balance_check


async def change_balance_game(user_id: int):
    cur.execute("UPDATE profile SET balance = balance - 2 WHERE user_id = ?", (user_id,))
    db.commit()


async def change_balance_win(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 4 WHERE user_id = ?", (user_id,))
    db.commit()

async def change_balance_draw(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 2 WHERE user_id = ?", (user_id,))
    db.commit()

async def change_balance_game_cups(user_id: int):
    cur.execute("UPDATE profile SET balance = balance - 3 WHERE user_id = ?", (user_id,))
    db.commit()

async def change_balance_game_wincups(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 12 WHERE user_id = ?", (user_id,))
    db.commit()

async def slot_win_100points(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 100 WHERE user_id = ?", (user_id,))
    db.commit()

async def slot_win_50points(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 50 WHERE user_id = ?", (user_id,))
    db.commit()

async def slot_win_25points(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 25 WHERE user_id = ?", (user_id,))
    db.commit()


async def slot_win_10points(user_id: int):
    cur.execute("UPDATE profile SET balance = balance + 10 WHERE user_id = ?", (user_id,))
    db.commit()


# async def getName(conn, user_id: int):
#     c = conn.cursor()
#     c.execute("SELECT name FROM profile WHERE)
#     result = c.fetchone()
#     if result:
#         return result[0]
#
# async def get_profile():
#     profile = cur.execute("SELECT name, balance FROM profile WHERE id = user_id")
#     name, balance = cur.fetchone()
#     print(f"Name: {name}    Age: {balance}")
#     db.commit()

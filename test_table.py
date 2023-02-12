import sqlite3


def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()

    for row in rows:
        print(row)

init_db()

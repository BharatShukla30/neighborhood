import sqlite3

def delete_table(name = 'users'):
    conn = sqlite3.connect('{}.db'.format(name))
    cur = conn.cursor()
    input = print('Are you sure you want to delete table {}?'.format(name))
    if input == 'yes':
        res = cur.execute("drop table {}".format(name)) 
        print(res)

def view_data_table_users():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()

    for row in rows:
        print(row)

view_data_table_users()
delete_table()

import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance balance NOT NULL
) 
''')

cursor.execute("CREATE INDEX IF NOT EXISTS ind_email ON Users (email)")
'''заполняем таблицу Users 10ю записями'''
# for i in range(1, 10+1):
#     cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
#                    (f"User{i}", f"example{i}@gmail.com", f"{i}0", 1000))
'''обновляем balance на значение 500 в каждой второй строке начиная с первой на 500'''
# for i in range(1, 10, 2):
#     cursor.execute("UPDATE Users SET balance = ? WHERE username = ?",
#                    (500, f"User{i}"))
'''удаляем каждую 3ю запись начиная с первой'''
# for i in range(1, 10+1, 3):
#     cursor.execute("DELETE FROM Users WHERE id = ?"  , (i,))
'''проводим выборку всех записей, где возраст больше 60 
в формате Имя: <username> | Почта: <email> | Возраст: <age> | Баланс: <balance>'''
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()
for user in users:
    username, email, age, balance = user
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")


connection.commit()
connection.close()

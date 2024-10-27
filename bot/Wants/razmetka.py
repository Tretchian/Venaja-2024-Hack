import sqlite3

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS words(
Id_Want INTEGER PRIMARY KEY,
Want_name TEXT NOT NULL,
Keywords TEXT NOT NULL)                           
              ''')

words = ['купить','приобрести', 'закупить', 'получить', 'заказать', 'взять']

for i in range(1, len(words)+1):
    cursor.execute('INSERT INTO words VALUES (?, ?, ?)', (i, 'купить', words[i-1]))
connection.commit()
connection.close()
import sqlite3

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Будем делать 1НФ
# Поля в таблице
# -----------wants_names_table----------------
# | Id_Wants                  | Wants_name  |
# |(Primary key)              | (TEXT)      |
# | (INTEGER AUTOINCREMENT)   | (NOT NULL)  |
# -------------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS wants_names (
    id_wants INTEGER PRIMARY KEY AUTOINCREMENT, 
    wants_name TEXT NOT NULL
               )                           
              ''')

# ----------------------kwords_wants----------------------------------------------------------
# | Id_Words                  | Id_wants                                          |Key_word  |
# |(Primary key)              | (INTEGER)                                         |(TEXT)    |
# | (INTEGER AUTOINCREMENT)   | (FOREIGN KEY) REFERENCES wants_names(wants_name)  |(NOT NULL)|
# --------------------------------------------------------------------------------------------

cursor.execute('''
CREATE TABLE IF NOT EXISTS kwords_wants (
    Id_words INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_wants INTEGER,
    Key_word TEXT NOT NULL,
	FOREIGN KEY (Id_wants) REFERENCES wants_names (wants_name)
               )                           
              ''')
# Пример добавления в таблицу намерений используя автоинкремент
# В Sqlite используется внутренний счетчик, который сбросить по необходимости получится, только снеся таблицу всю
# words = ["купить"]
# for i in words:
#     cursor.execute("INSERT INTO wants_names(wants_name) VALUES(?)", (i,))


# words = ['купить','приобрести', 'закупить', 'получить', 'заказать', 'взять']
# for i in words:
#     cursor.execute('INSERT INTO kwords_wants(Id_wants, Key_word) VALUES (?, ?)', (1, i))

connection.commit()
connection.close()


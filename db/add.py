import sqlite3

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('db/Main_DB.db')
cursor = connection.cursor()
# Добавление в kwords_wants
kwords_wants =[
['купить', 'приобрести', 'закупить', 'прикупить', 'докупить', 'покупать', 'скупить', 'заказать', 'урвать'],
['поменять', 'сменить', 'изменить', 'переменять', 'переменить', 'сменять', 'пересмотреть'],
['привет', 'прив', 'здраствуйте', 'йоу', 'куку', 'здаров', 'приветик', 'салют', 'ку'],
['до свидания', 'прощайте', 'покасики', 'пок', 'покиноки', 'бб', 'байбай', 'гудбай']
]

for i in range(0, len(kwords_wants)):
    for j in kwords_wants[i]:
        cursor.execute("INSERT INTO kwords_wants (Id_wants, Key_word) VALUES (?, ?)", (i+1, j))

# Добавление в wants_names
Wants_name = ['купить', 'поменять', 'привет', 'пока']
for i in Wants_name:
    cursor.execute("INSERT INTO wants_names(wants_name) VALUES (?)", (i,))
    
connection.commit()
connection.close()
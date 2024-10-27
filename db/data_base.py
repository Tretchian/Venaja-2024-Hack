import sqlite3

user_states = {}  # Словарь для хранения состояния каждого пользователя


# Функция для генерации следующего доступного Pact_ID
def generate_pact_id() -> str:
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()

    # Начинаем поиск с 516_000_000
    cursor.execute("SELECT IFNULL(MAX(ID_Pact), 516000000) + 1 FROM Client WHERE ID_Pact LIKE '516%'")
    next_id = cursor.fetchone()[0]

    conn.close()
    return next_id if str(next_id).startswith('516') else None


# Функция для записи данных нового пользователя в базу данных
def register_user(user_info: list):
    TG_ID = user_info[0]
    Name = user_info[1]
    Surname = user_info[2]
    Middlename = user_info[3]
    PhoneNumber = user_info[4]
    Adress = user_info[5]

    ID_Pact = generate_pact_id()
    if ID_Pact:
        conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Client
                       (TG_ID,
                       ID_Pact,
                       Name,
                       Surname,
                       Middlename,
                       PhoneNumber,
                       Address)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''',
                       (TG_ID,
                        ID_Pact,
                        Name,
                        Surname,
                        Middlename,
                        PhoneNumber,
                        Adress))
        conn.commit()
        conn.close()


# Проверка наличия Pact_ID в базе данных
def check_user_in_db(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Client WHERE ID_Pact = ?", (ID_Pact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

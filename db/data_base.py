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
        return ID_Pact


# Проверка наличия Pact_ID в базе данных
def check_user_in_db(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Client WHERE ID_Pact = ?", (ID_Pact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_name_by_pact_id(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT Name FROM Client WHERE ID_Pact = ?", (ID_Pact,))
    result = cursor.fetchone()
    
    conn.close()
    
    name = result[0] if result else None
    return name


def check_user_services_and_tariffs(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()

    # Находим все ID_Tariff и ID_Service для данного Pact_ID
    cursor.execute("SELECT ID_Tariff, ID_Service FROM Client WHERE ID_Pact = ?", (ID_Pact,))
    results = cursor.fetchall()

    if not results:
        conn.close()
        return "Пользователь с таким Pact_ID не найден."

    # Собираем уникальные Tariff_ID и ID_Service
    tariff_ids = {row[0] for row in results if row[0] is not None}
    service_ids = {row[1] for row in results if row[1] is not None}

    # Проверка на наличие подключений
    if not tariff_ids and not service_ids:
        conn.close()
        return "У вас не подключены ни тарифы, ни услуги."

    # Получаем названия подключённых тарифов
    tariff_names = []
    if tariff_ids:
        cursor.execute("SELECT Tariff_Name FROM Tariffs WHERE ID_Tariff IN ({})".format(", ".join("?" * len(tariff_ids))), tuple(tariff_ids))
        tariff_names = [row[0] for row in cursor.fetchall()]

    # Получаем названия подключённых услуг
    service_names = []
    if service_ids:
        cursor.execute("SELECT Service_Name FROM Services WHERE ID_Service IN ({})".format(", ".join("?" * len(service_ids))), tuple(service_ids))
        service_names = [row[0] for row in cursor.fetchall()]

    conn.close()

    # Формируем итоговое сообщение
    message = ""
    if tariff_names:
        message += "Ваши подключённые тарифы: " + ", ".join(tariff_names) + "."
    else:
        message += "У вас не подключены тарифы."
        
    if service_names:
        message += "\nВаши подключённые услуги: " + ", ".join(service_names) + "."
    else:
        message += "\nУ вас не подключены услуги."

    return message
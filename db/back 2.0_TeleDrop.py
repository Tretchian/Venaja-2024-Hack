import sqlite3

# Словарь для хранения состояния каждого пользователя
user_states = {}

# Функция для генерации следующего доступного Pact_ID
def generate_pact_id():
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Начинаем поиск с 516000000
    cursor.execute("SELECT IFNULL(MAX(ID_Pact), 516000000) + 1 FROM Client WHERE ID_Pact LIKE '516%'")
    next_id = cursor.fetchone()[0]
    
    conn.close()
    return next_id if str(next_id).startswith('516') else None

# Функция для записи данных нового пользователя в базу данных
def register_user(TG_ID, ID_Pact, Name, Surname, Middlename, PhoneNumber, Address):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO Client (TG_ID, ID_Pact, Name, Surname, Middlename, PhoneNumber, Address) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (TG_ID, ID_Pact, Name, Surname, Middlename, PhoneNumber, Address))
    conn.commit()
    conn.close()

# Обработчик команды /start
def start_message(user_id):
    user_states[user_id] = 'start'  # Устанавливаем начальное состояние
    return "Добро пожаловать! Вы зарегистрированы в базе данных? (да/нет)"

# Обработчик текстовых сообщений для проверки регистрации
def handle_message(user_id, text):
    text = text.lower()

    # Проверка состояния пользователя
    if user_id in user_states:
        state = user_states[user_id]

        # Возврат на предыдущий этап
        if text == "назад":
            if state in ["registration", "entering_pact_id"]:
                user_states[user_id] = "start"
                return "Выберите, зарегистрированы ли вы в базе данных? (да/нет)"

        # Обработка ответа на регистрацию
        if state == "start":
            if text == "да":
                user_states[user_id] = "entering_pact_id"
                return "Пожалуйста, введите ваш Pact_ID для проверки."
            elif text == "нет":
                user_states[user_id] = "registration"
                return "Пожалуйста, введите свои данные в формате: Имя, Фамилия, Отчество (если есть), Телефон, Адрес."
            else:
                return "Пожалуйста, ответьте 'да' или 'нет'."

        # Проверка введенного Pact_ID
        elif state == "entering_pact_id":
            return check_pact_id(user_id, text)

        # Функция для обработки регистрации
        elif state == "registration":
            return handle_registration(user_id, text)

# Проверка введенного Pact_ID
def check_pact_id(user_id, ID_Pact):
    if ID_Pact.lower() == "назад":
        user_states[user_id] = "start"
        return "Выберите, зарегистрированы ли вы в базе данных? (да/нет)"

    try:
        ID_Pact = int(ID_Pact)  # Преобразуем текст в целое число
        if check_user_in_db(ID_Pact):
            user_states.pop(user_id)  # Сбрасываем состояние после успешного входа
            return "Добро пожаловать! Вы успешно вошли в систему."
        else:
            return "Пользователь с таким Pact_ID не найден. Пожалуйста, зарегистрируйтесь."
    except ValueError:
        return "Пожалуйста, введите корректный Pact_ID."

# Функция для обработки регистрации
def handle_registration(user_id, text):
    if text.lower() == "назад":
        user_states[user_id] = "start"
        return "Выберите, зарегистрированы ли вы в базе данных? (да/нет)"

    parts = [part.strip() for part in text.split(",")]
    
    if len(parts) >= 4:
        TG_ID = user_id  # Здесь вместо Telegram username используется ID пользователя
        Name = parts[0]
        Surname = parts[1]
        Middlename = parts[2] if len(parts) > 4 else None  # Отчество может отсутствовать
        PhoneNumber = parts[3]
        Address = ', '.join(part.strip() for part in parts[4:])  # Собираем адрес из оставшихся частей

        # Генерация Pact_ID
        ID_Pact = generate_pact_id()
        if ID_Pact:
            # Запись данных в базу
            register_user(TG_ID, ID_Pact, Name, Surname, Middlename, PhoneNumber, Address)
            user_states.pop(user_id)  # Сбрасываем состояние после успешной регистрации
            return f"Вы успешно зарегистрированы! Ваш Pact_ID: {ID_Pact}"
        else:
            return "Не удалось сгенерировать уникальный Pact_ID. Пожалуйста, попробуйте позже."
    else:
        return "Пожалуйста, введите все данные корректно в формате: Имя, Фамилия, Отчество (если есть), Телефон, Адрес."

# Проверка наличия Pact_ID в базе данных
def check_user_in_db(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Client WHERE ID_Pact = ?", (ID_Pact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

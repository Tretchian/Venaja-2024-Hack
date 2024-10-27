import sqlite3
import telebot
import re

bot = telebot.TeleBot("7842088143:AAHv_xVjFenL-FMRgdKVCJn31YP0upYZd5c")
user_states = {}  # Словарь для хранения состояния каждого пользователя

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
@bot.message_handler(commands=['start'])
def start_message(message):
    user_states[message.chat.id] = 'start'  # Устанавливаем начальное состояние
    bot.send_message(message.chat.id, "Добро пожаловать! Вы зарегистрированы в базе данных? (да/нет)")

# Обработчик текстовых сообщений для проверки регистрации
@bot.message_handler(content_types=['text'])
def handle_message(message):
    user_id = message.chat.id
    text = message.text.lower()

    # Проверка состояния пользователя
    if user_id in user_states:
        state = user_states[user_id]

        # Возврат на предыдущий этап
        if text == "назад":
            if state in ["registration", "entering_pact_id"]:
                user_states[user_id] = "start"
                bot.send_message(user_id, "Выберите, зарегистрированы ли вы в базе данных? (да/нет)")
            return  # Выход из функции

        # Обработка ответа на регистрацию
        if state == "start":
            if text == "да":
                user_states[user_id] = "entering_pact_id"
                bot.send_message(user_id, "Пожалуйста, введите ваш Pact_ID для проверки.")
                bot.register_next_step_handler(message, check_pact_id)

            elif text == "нет":
                user_states[user_id] = "registration"
                bot.send_message(user_id, "Пожалуйста, введите свои данные в формате: Имя, Фамилия, Отчество (если есть), Телефон, Адрес.")
                bot.register_next_step_handler(message, handle_registration)

            else:
                bot.send_message(user_id, "Пожалуйста, ответьте 'да' или 'нет'.")

        # Проверка введенного Pact_ID
        elif state == "entering_pact_id":
            check_pact_id(message)

        # Функция для обработки регистрации
        elif state == "registration":
            handle_registration(message)

# Проверка введенного Pact_ID
def check_pact_id(message):
    user_id = message.chat.id
    ID_Pact = message.text  # Сохраняем текст для дальнейшей проверки

    if ID_Pact.lower() == "назад":
        user_states[user_id] = "start"
        bot.send_message(user_id, "Выберите, зарегистрированы ли вы в базе данных? (да/нет)")
        return  # Выход из функции

    try:
        ID_Pact = int(ID_Pact)  # Преобразуем текст в целое число
        if check_user_in_db(ID_Pact):
            bot.send_message(user_id, "Добро пожаловать! Вы успешно вошли в систему.")
            user_states.pop(user_id)  # Сбрасываем состояние после успешного входа
        else:
            bot.send_message(user_id, "Пользователь с таким Pact_ID не найден. Пожалуйста, зарегистрируйтесь.")
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введите корректный Pact_ID.")

# Функция для обработки регистрации
def handle_registration(message):
    user_id = message.chat.id

    if message.text.lower() == "назад":
        user_states[user_id] = "start"
        bot.send_message(user_id, "Выберите, зарегистрированы ли вы в базе данных? (да/нет)")
        return  # Выход из функции

    pattern = r'^\s*([^,]+),\s*([^,]+),\s*([^,]*),\s*([^,]+),\s*(.*)$'

    match = re.match(pattern, message.text)
    if match:
        Name, Surname, Middlename, PhoneNumber, Address = match.groups()
        TG_ID = message.from_user.username
        # Генерация Pact_ID
        ID_Pact = generate_pact_id()
        if ID_Pact:
            # Запись данных в базу
            register_user(TG_ID, ID_Pact, Name, Surname, Middlename, PhoneNumber, Address)
            bot.send_message(user_id, f"Вы успешно зарегистрированы! Ваш Pact_ID: {ID_Pact}")
            user_states.pop(user_id)  # Сбрасываем состояние после успешной регистрации
        else:
            bot.send_message(user_id, "Не удалось сгенерировать уникальный Pact_ID. Пожалуйста, попробуйте позже.")
    else:
        bot.send_message(user_id, "Пожалуйста, введите все данные корректно в формате: Имя, Фамилия, Отчество (если есть), Телефон, Адрес.")

# Проверка наличия Pact_ID в базе данных
def check_user_in_db(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Client WHERE ID_Pact = ?", (ID_Pact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Запуск бота
bot.polling(none_stop=True)

#Добавить защиту от Дроптейбла
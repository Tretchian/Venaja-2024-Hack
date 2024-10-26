import sqlite3
import telebot

bot = telebot.TeleBot("7842088143:AAHv_xVjFenL-FMRgdKVCJn31YP0upYZd5c")
user_state = {}  # Словарь для хранения состояния каждого пользователя

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Для регистрации отправьте сообщение, начинающееся с "Регистрация".')

# Проверка существующего ID_Pact в базе данных
def check_pact_id_exists(ID_Pact):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Client WHERE ID_Pact = ?', (ID_Pact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для проверки существующей услуги
def service_exists(ID_Pact, TG_ID, ServiceName):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Client WHERE ID_Pact = ? AND TG_ID = ? AND ID_Service = ?', (ID_Pact, TG_ID, ServiceName))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для проверки существующего тарифа
def tariff_exists(ID_Pact, TG_ID, ID_Tariff):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Client WHERE ID_Pact = ? AND TG_ID = ? AND ID_Tariff = ?', (ID_Pact, TG_ID, ID_Tariff))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для записи данных об услуге
def log_Client_Service(ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Service):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Client (ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Service) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Service))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с БД: {e}")
    finally:
        conn.close()

# Функция для записи данных о тарифе
def log_Client_Tariff(ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Tariff):
    conn = sqlite3.connect('db/Main_DB.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Client (ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Tariff) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Tariff))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с БД: {e}")
    finally:
        conn.close()

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_message(message):
    user_id = message.chat.id
    text = message.text.lower()

    # Проверка состояния пользователя
    if user_id in user_state:
        state = user_state[user_id]

        # Команда для возврата на предыдущий этап
        if text in ["/назад", "назад"]:
            if state == 'awaiting_service_data' or state == 'awaiting_tariff_data':
                user_state[user_id] = 'awaiting_choice'
                bot.send_message(user_id, "Выберите тип регистрации: 'Услуга' или 'Тариф'.")
            elif state == 'awaiting_choice':
                user_state.pop(user_id)  # Сбрасываем состояние для возврата к началу
                bot.send_message(user_id, "Для регистрации отправьте сообщение, начинающееся с 'Регистрация'.")
            elif state == 'checking_pact_id':
                user_state.pop(user_id)  # Возвращаемся к стартовому состоянию
                bot.send_message(user_id, "Для начала введите 'Регистрация'.")
            return

        # Проверка Pact_ID
        if state == 'checking_pact_id':
            try:
                ID_Pact = int(text)
                if check_pact_id_exists(ID_Pact):
                    bot.send_message(user_id, "Ваш ID_Pact найден в системе. Вы можете продолжить.")
                    user_state.pop(user_id)
                else:
                    bot.send_message(user_id, "ID_Pact не найден. Проверьте данные и попробуйте снова.")
            except ValueError:
                bot.send_message(user_id, "ID_Pact должен быть числом. Попробуйте еще раз.")

        # Обработка выбора типа регистрации
        elif state == 'awaiting_choice':
            if text == "услуга":
                user_state[user_id] = 'awaiting_service_data'
                bot.send_message(user_id, "Введите данные для услуги в формате: ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Service")
            elif text == "тариф":
                user_state[user_id] = 'awaiting_tariff_data'
                bot.send_message(user_id, "Введите данные для тарифа в формате: ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Tariff")
            else:
                bot.send_message(user_id, "Пожалуйста, выберите 'Услуга' или 'Тариф'.")

        # Обработка данных для услуги
        elif state == 'awaiting_service_data':
            parts = [part.strip() for part in text.split(",")]
            if len(parts) == 8:
                try:
                    ID_Pact = int(parts[0])
                    TG_ID = parts[1]
                    Name = parts[2]
                    Surname = parts[3]
                    Middlename = parts[4]
                    PhoneNumber = parts[5]
                    Address = parts[6]
                    ID_Service = int(parts[7])

                    if service_exists(ID_Pact, TG_ID, ID_Service):
                        bot.reply_to(message, "Услуга уже подключена!")
                    else:
                        log_Client_Service(ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Service)
                        bot.reply_to(message, "Данные об услуге успешно сохранены!")
                        user_state.pop(user_id)
                except ValueError:
                    bot.reply_to(message, "Пожалуйста, убедитесь, что ID_Pact и ID_Service являются числами.")
            else:
                bot.reply_to(message, "Пожалуйста, отправьте данные в формате: ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Service")

        # Обработка данных для тарифа
        elif state == 'awaiting_tariff_data':
            parts = [part.strip() for part in text.split(",")]
            if len(parts) == 8:
                try:
                    ID_Pact = int(parts[0])
                    TG_ID = parts[1]
                    Name = parts[2]
                    Surname = parts[3]
                    Middlename = parts[4]
                    PhoneNumber = parts[5]
                    Address = parts[6]
                    ID_Tariff = int(parts[7])

                    if tariff_exists(ID_Pact, TG_ID, ID_Tariff):
                        bot.reply_to(message, "Тариф уже подключен!")
                    else:
                        log_Client_Tariff(ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Tariff)
                        bot.reply_to(message, "Данные о тарифе успешно сохранены!")
                        user_state.pop(user_id)
                except ValueError:
                    bot.reply_to(message, "Пожалуйста, убедитесь, что ID_Pact и ID_Tariff являются числами.")
            else:
                bot.reply_to(message, "Пожалуйста, отправьте данные в формате: ID_Pact, TG_ID, Name, Surname, Middlename, PhoneNumber, Address, ID_Tariff")

    else:
        # Начало регистрации
        if text.startswith("регистрация"):
            user_state[user_id] = 'awaiting_choice'
            bot.send_message(user_id, "Выберите тип регистрации: 'Услуга' или 'Тариф'.")
        elif text == "да":
            user_state[user_id] = 'checking_pact_id'
            bot.send_message(user_id, "Введите ваш Pact_ID для проверки.")
        else:
            bot.reply_to(message, "Для регистрации начните сообщение с ключевого слова 'Регистрация'.")

# Запуск бота
bot.polling(none_stop=True)

import telebot
import requests
import re
from telebot import types


# Токен бота
bot_token = '7659124438:AAGJEiu7fVOET0Vy_hypEfdq0YZTJ25xwJI'


# Объект тг-бот
bot = telebot.TeleBot(bot_token)


welcome_text = 'Здраствуйте, я бот-помощник ТТК, Чтобы войти напишите "Войти как клиент ТТК". Если хотите заключить новый догвор, пожалуйста напишите "Заключить новый договор"'
user_contract_enter_text = 'Пожалуйста введите свой номер договора, чтобы я понял кто вы'
user_contact_info_text = 'Укажите свой контактный номер и адрес для подключения услуги'
bot_not_understand_text = 'Извини, я тебя не понял. Давай еще раз'
user_wrong = 'Неправильно, попробуйте еще раз'


# Клавиатура возврата в начало
def keyboard_back_to_welcome():
    # Инициализация клавиатуры в один ряд
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # Кнопка «Назад»
    key_back = types.InlineKeyboardButton(text='Назад',
                                          callback_data='back_to_start')
    # Добавялем кнопку
    keyboard.add(key_back)
    return keyboard


# Клавиатура приветственная
def keyboard_welcoming():
    # Инициализация клавиатуры в один ряд
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # Кнопка «Войти как клиент ТТК»
    key_ttk_user_enter = types.InlineKeyboardButton(text='1. Войти как клиент ТТК',
                                                    callback_data='enter_as_client')
    # Кнопка «Заключить новый договор»
    key_ttk_user_conclude_contract = types.InlineKeyboardButton(text='2. Заключить новый договор',
                                                                callback_data='conclude_contract')
    # Добавляем кнопки в клавиатуру
    keyboard.add(key_ttk_user_enter, key_ttk_user_conclude_contract)
    return keyboard


# Сохранение аудио
def voice_message_download(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_token,
                                                                          file_info.file_path))
    with open(f'{message.from_user.id}.ogg', 'wb') as f:
        f.write(file.content)


# Конструктор отправки сообщения и следущего шага
def next_step_and_output_message(message,
                                 user_output_text,
                                 keyboard,
                                 next_func):
    # Отправка сообщения пользователю
    bot.send_message(message.from_user.id,
                     text=user_output_text,
                     reply_markup=keyboard)
    # Указание следующий функции
    bot.register_next_step_handler(message, next_func)


# Конструктор отправки сообщения и следющего шага для кнопок
def next_step_and_output_message_callback(call,
                                          user_output_text,
                                          keyboard,
                                          next_func):
    # Очистка предыдущих обработчиков
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    # Отправка сообщения пользователю
    bot.send_message(call.message.chat.id,
                     user_output_text,
                     reply_markup=keyboard)
    # Следующий запрос
    bot.register_next_step_handler(call.message,
                                   next_func)


# Паттерн телефона
phone_pattern = re.compile(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
'''
"+1 (555) 123-4567"
"555-123-4567"
"555 123 4567"
"+44 (0) 20 1234 5678"
"02012345678"
'''


# Проверка на номер телефона в строке
def validate_phone_number(regex, phone_number):
    match = re.search(regex, phone_number)
    if match:
        return True
    return False


# Вход как клиент ТТК
def enter_as_client(message):

    # Если найден номер догвора по маске вход удачен
    if re.search(r'[516]+[0-9]{6}', message.text):
        print('succses_enter')
        next_step_and_output_message(message,
                                     welcome_text,
                                     keyboard_welcoming(),
                                     user_first_choice)

    # Возврат назад
    elif message.text.lower() == 'назад':
        next_step_and_output_message(message,
                                     welcome_text,
                                     keyboard_welcoming(),
                                     user_first_choice)

    # Неправильный ввод и повтор ввода
    else:
        next_step_and_output_message(message,
                                     user_wrong,
                                     keyboard_back_to_welcome(),
                                     enter_as_client)


# Заключение нового контракта
def conclude_contract(message):

    # Валидация
    if validate_phone_number(phone_pattern, message.text):

        # Находим номер в строке
        phone_number = re.search(phone_pattern, message.text)[0]

        # Убираем из текста номер
        adress = message.text.replace(phone_number, '', 1)

        # Убираем ненужные символы
        adress_filtered = "".join(c for c in adress if c.isalpha())

        print(phone_number)
        print(adress_filtered)
        next_step_and_output_message(message,
                                     welcome_text,
                                     keyboard_welcoming(),
                                     user_first_choice)

    # Возврат назад
    elif message.text.lower() == 'назад':
        next_step_and_output_message(message,
                                     welcome_text,
                                     keyboard_welcoming(),
                                     user_first_choice)

    # Неправильный ввод и повтор ввода
    else:
        next_step_and_output_message(message,
                                     user_wrong,
                                     keyboard_back_to_welcome(),
                                     conclude_contract)


# Обработка начала диалога
@bot.message_handler(commands=['start'])
# Вывод приветственного сообщения
def welcome_message_output(message):
    # Отправка сообщения пользователю
    bot.send_message(message.from_user.id,
                     text=welcome_text,
                     reply_markup=keyboard_welcoming())


@bot.message_handler(content_types=['voice'])   # Обработка голосовых
def start_voice_message(message):
    voice_message_download(message)


# Обработка текстовых
@bot.message_handler(content_types=['text'])
# Начальное сообщение
def user_first_choice(message):
    if message.text in ['1', 'Войти как клиент ТТК', 'Войти', 'войти']:
        next_step_and_output_message(message,
                                     user_contract_enter_text,
                                     keyboard_back_to_welcome(),
                                     enter_as_client)
    elif message.text in ['2', 'Заключить новый договор']:
        next_step_and_output_message(message,
                                     user_contact_info_text,
                                     keyboard_back_to_welcome(),
                                     conclude_contract)
    else:
        next_step_and_output_message(message,
                                     bot_not_understand_text,
                                     None,
                                     user_first_choice)


# Обработка нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callbacker(call):
    if call.data == 'enter_as_client':
        next_step_and_output_message_callback(call,
                                              user_contract_enter_text,
                                              keyboard_back_to_welcome(),
                                              enter_as_client)

    elif call.data == 'conclude_contract':
        next_step_and_output_message_callback(call,
                                              user_contact_info_text,
                                              keyboard_back_to_welcome(),
                                              conclude_contract)

    elif call.data == 'back_to_start':
        next_step_and_output_message_callback(call,
                                              welcome_text,
                                              keyboard_welcoming(),
                                              user_first_choice)


bot.polling(none_stop=True)

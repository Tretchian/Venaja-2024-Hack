import telebot
import requests
import re
from telebot import types

bot_token = '7659124438:AAGJEiu7fVOET0Vy_hypEfdq0YZTJ25xwJI' # Токен бота

bot = telebot.TeleBot(bot_token) # Объект тг-бот

welcome_text = 'Здраствуйте, я бот-помощник ТТК, Чтобы войти напишите "Войти как клиент ТТК". Если хотите заключить новый догвор, пожалуйста напишите "Заключить новый договор"' 
user_contract_enter_text = 'Пожалуйста введите свой номер договора, чтобы я понял кто вы' 
user_contact_info_text = 'Укажите свой контактный номер и адрес для подключения услуги' 
bot_not_understand_text = 'Извини, я тебя не понял. Давай еще раз'
user_wrong = 'Неправильно, попробуйте еще раз'


def back_to_start_keyboard(): # Клавиатура возврата в начало
    keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры в один ряд
    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back_to_start') # Кнопка «Назад»
    keyboard.add(key_back) # Добавялем кнопку 
    return keyboard


def welcome_keyboard(): # Клавиатура приветственная
    keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры в один ряд
    key_ttk_user_enter = types.InlineKeyboardButton(text='1. Войти как клиент ТТК', callback_data='enter_as_client') # Кнопка «Войти как клиент ТТК»
    key_ttk_user_conclude_contract= types.InlineKeyboardButton(text='2. Заключить новый договор', callback_data='conclude_contract') # Кнопка «Заключить новый договор»
    keyboard.add(key_ttk_user_enter, key_ttk_user_conclude_contract) # Добавляем кнопки в клавиатуру
    return keyboard


def voice_message_download(message): # Сохранение аудио
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_token, file_info.file_path))
    with open(f'{message.from_user.id}.ogg','wb') as f:
        f.write(file.content)


def next_step_and_output_message(message, user_output_text, keyboard, next_func): # Конструктор отправки сообщения и следущего шага
    bot.send_message(message.from_user.id, text=user_output_text, reply_markup=keyboard) # Отправка сообщения пользователю
    bot.register_next_step_handler(message, next_func) # Указание следующий функции


phone_pattern = re.compile(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}") # Паттерн телефона
''' 
"+1 (555) 123-4567"
"555-123-4567"
"555 123 4567"
"+44 (0) 20 1234 5678"
"02012345678"
'''
def validate_phone_number(regex, phone_number): # Проверка на номер телефона в строке
    match = re.search(regex, phone_number)
    if match:
        return True
    return False


@bot.message_handler(commands=['start'])    # Обработка начала диалога
def welcome_message_output(message):   # Вывод приветственного сообщения
    bot.send_message(message.from_user.id, text=welcome_text, reply_markup=welcome_keyboard()) # Отправка сообщения пользователю


@bot.message_handler(content_types=['voice'])   # Обработка голосовых
def start_voice_message(message):
    voice_message_download(message)


@bot.message_handler(content_types=['text'])  # Обработка текстовых 
def start_text_message(message): # Начальное сообщение 
    if message.text in ['1', 'Войти как клиент ТТК', 'Войти', 'войти']:
        next_step_and_output_message(message, user_contract_enter_text, back_to_start_keyboard(), enter_as_client)
        
    elif message.text in ['2', 'Заключить новый договор']:
        next_step_and_output_message(message, user_contact_info_text, back_to_start_keyboard(), conclude_contract)

    else: 
        next_step_and_output_message(message, bot_not_understand_text, None, start_text_message)


def enter_as_client(message): # Вход как клиент ТТК
    print(message.text)
    if re.search(r'[516]+[0-9]{6}', message.text):
        print('succses_enter') 

    elif message.text.lower() == 'назад': # Возврат назад 
        next_step_and_output_message(message, welcome_text, welcome_keyboard(), start_text_message)

    else: # Неправильный ввод и повтор ввода 
        next_step_and_output_message(message, user_wrong, back_to_start_keyboard(), enter_as_client)
        

def conclude_contract(message): # Заключение нового контракта

    if validate_phone_number(phone_pattern, message.text): # Валидация
        phone_number = re.search(phone_pattern, message.text)[0] # Находим номер в строке
        adress = message.text.replace(phone_number, '', 1) # Убираем из текста номер
        adress_filtered = "".join(c for c in adress if c.isalpha()) # Убираем ненужные символы 

        print(phone_number)
        print(adress_filtered)

    elif message.text.lower() == 'назад': # Возврат назад 
        next_step_and_output_message(message, welcome_text, welcome_keyboard(), start_text_message) #

    else: # Неправильный ввод и повтор ввода 
        next_step_and_output_message(message, user_wrong, back_to_start_keyboard(), conclude_contract) #






'''
@bot.callback_query_handler(func=lambda call: True) # Обработка нажатия на кнопку
def callback_worker(call): # обрабатывем кнопки
    if call.data == "enter_as_client": # Если пользователь зарегистрирован заходим сюда
        bot.register_next_step_handler(call, enter_as_client)

    elif call.data == "conclude_contract": # Если хочет заключить договор 
        bot.register_next_step_handler(call, enter_as_client)
        
    elif call.data == "back_to_start": # Возврат обратно
        welcome_message_output(call) 
'''

bot.polling(none_stop=True)


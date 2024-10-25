import telebot
from telebot import types 

bot = telebot.TeleBot('7659124438:AAGJEiu7fVOET0Vy_hypEfdq0YZTJ25xwJI') # Токен бота


@bot.message_handler(commands=['start'])    # Обработка начала диалога

def welcome_message(message):   # вывод приветственного сообщения

    keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры
    
    key_ttk_user_enter = types.InlineKeyboardButton(text='1. Войти как клиент ТТК', callback_data='enter') # Кнопка «Войти как клиент ТТК»
    
    key_ttk_user_conclude_contract= types.InlineKeyboardButton(text='2. Заключить новый договор', callback_data='conclude') # Кнопка «Заключить новый договор»
    
    keyboard.add(key_ttk_user_enter, key_ttk_user_conclude_contract) # Добавляем кнопки в клавиатуру
    
    welcome_text = 'Здраствуйте, я бот помощник ТТК, если вы пользователь выберите 1. Если вы не пользуетесь услугами, пожалуйста выберите 2' # Приветственный 
    bot.send_message(message.from_user.id, text=welcome_text, reply_markup=keyboard) # Отправка сообщения пользователю


@bot.callback_query_handler(func=lambda call: True) # Обработка нажатия на кнопку

def callback_worker(call): # обрабатывем кнопки
    if call.data == "enter": 

        user_input_text = 'Пожалуйста введите свой номер договора, чтобы я понял кто вы' # Текст для вывода

        keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='back') # Кнопка «Назад»
        keyboard.add(key_back) # Добавялем кнопку 

        bot.send_message(call.from_user.id, text=user_input_text, reply_markup=keyboard) # Отправка сообщения пользователю

    elif call.data == "conclude":
        user_input_text = 'Укажите свой контактный номер и адрес для подключения услуги' # Текст для вывода

        keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='back') # Кнопка «Назад»
        keyboard.add(key_back) # Добавялем кнопку 

        bot.send_message(call.from_user.id, text=user_input_text, reply_markup=keyboard) # Отправка сообщения пользователю

    if call.data == "back":
        welcome_message(call) 



bot.polling(none_stop=True)

import telebot
import requests
from telebot import types 

bot_token ='7659124438:AAGJEiu7fVOET0Vy_hypEfdq0YZTJ25xwJI'

bot = telebot.TeleBot(bot_token) # Токен бота

def back_to_start():
    keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры в один ряд
    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back_to_start') # Кнопка «Назад»
    keyboard.add(key_back) # Добавялем кнопку 
    return keyboard

def welcome_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1); # Инициализация клавиатуры в один ряд
    key_ttk_user_enter = types.InlineKeyboardButton(text='1. Войти как клиент ТТК', callback_data='enter_as_client') # Кнопка «Войти как клиент ТТК»
    key_ttk_user_conclude_contract= types.InlineKeyboardButton(text='2. Заключить новый договор', callback_data='conclude_contract') # Кнопка «Заключить новый договор»
    keyboard.add(key_ttk_user_enter, key_ttk_user_conclude_contract) # Добавляем кнопки в клавиатуру
    return keyboard

def voice_message_download(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_token, file_info.file_path))
    with open(f'{message.from_user.id}.ogg','wb') as f:
        f.write(file.content)



@bot.message_handler(commands=['start'])    # Обработка начала диалога
def welcome_message_output(message):   # Вывод приветственного сообщения

    welcome_text = 'Здраствуйте, я бот-помощник ТТК, Чтобы войти выберите или напишите "Войти как клиент ТТК". Если вы не пользуетесь услугами ТТК и хотите заключить новый догвор, пожалуйста выберите или напишите "Заключить новый договор"' # Приветственный 
    
    bot.send_message(message.from_user.id, text=welcome_text, reply_markup=welcome_keyboard()) # Отправка сообщения пользователю


@bot.message_handler(content_types=['text','voice'])  

def messages(message):
    if message.voice:
        voice_message_download(message)
    if message.text:
        if message.text in ['1', 'Войти как клиент ТТК', 'Войти', 'войти']:

            user_output_text = f'Пожалуйста введите свой номер договора, чтобы я понял кто вы' # Текст для вывода
            bot.send_message(message.from_user.id, text=user_output_text, reply_markup=back_to_start()) # Отправка сообщения пользователю
            bot.register_next_step_handler(message, enter_as_client)

        elif message.text in ['2', 'Заключить новый договор']:

            user_output_text = f'Укажите свой контактный номер и адрес для подключения услуги' # Текст для вывода
            bot.send_message(message.from_user.id, text=user_output_text, reply_markup=back_to_start()) # Отправка сообщения пользователю
            bot.register_next_step_handler(message, conclude_contract)

        else: 
            print(f'{message.from_user.id} чето другое')

def enter_as_client(message):
        user_wrong = 'неправильный номер договора'

        if len(message.text) == 9 and message.text[:6] == '516':
            print(message.text)
        else:
            bot.send_message(message.from_user.id, text=user_wrong, reply_markup=back_to_start())     

def conclude_contract(message): 
    user_wrong = 'неправильный номер телефона'

    if len(message.text) == 11 and message.text[0] == '+':
        print(message.text)
    else:
        bot.send_message(message.from_user.id, text=user_wrong, reply_markup=back_to_start())

@bot.callback_query_handler(func = lambda call: True) # Обработка нажатия на кнопку
def callback_worker(call): # обрабатывем кнопки
    if call.data == "enter_as_client": # Если пользователь зарегистрирован заходим сюда
        bot.register_next_step_handler(call.message, enter_as_client)

    elif call.data == "conclude_contract": # Если хочет заключить договор 
        bot.register_next_step_handler(call.message, enter_as_client)
        
    elif call.data == "back_to_start": # Возврат обратно
        welcome_message_output(call) 

bot.polling(none_stop=True)

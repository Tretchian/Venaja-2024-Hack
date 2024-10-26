import telebot
import requests
from telebot import types 

bot_token ='7659124438:AAGJEiu7fVOET0Vy_hypEfdq0YZTJ25xwJI'

bot = telebot.TeleBot(bot_token) # Токен бота


def client_data_sender():
     @bot.message_handler(content_types=['text'])    # Обработка ввода
     def send_data(message):
        print(message.text, "1")

def contract_data_sender():
    @bot.message_handler(content_types=['text'])    # Обработка ввода
    def send_data(message):
        print(message.text, "2")
    
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
    with open(f'{message.from_user.username}_{message.from_user.id}.ogg','wb') as f:
        f.write(file.content)

def text_(message):
    print(message.text)


@bot.message_handler(commands=['start'])    # Обработка начала диалога
def welcome_message_output(message):   # Вывод приветственного сообщения

    welcome_text = 'Здраствуйте, я бот помощник ТТК, если вы пользователь ТТК выберите 1. Если вы не пользуетесь услугами, пожалуйста выберите 2' # Приветственный 
    
    bot.send_message(message.from_user.id, text=welcome_text, reply_markup=welcome_keyboard()) # Отправка сообщения пользователю


@bot.message_handler(content_types=['text','voice'])  
def first_message(message):
    if message.voice:
        voice_message_download(message)
    if message.text:
         text_
        


@bot.callback_query_handler(func=lambda call: True) # Обработка нажатия на кнопку
def callback_worker(call): # обрабатывем кнопки
    if call.data == "enter_as_client": # Если пользователь зарегистрирован заходим сюда

        user_output_text = 'Пожалуйста введите свой номер договора, чтобы я понял кто вы' # Текст для вывода

        bot.send_message(call.from_user.id, text=user_output_text, reply_markup=back_to_start()) # Отправка сообщения пользователю
                
        client_data_sender()
       

    elif call.data == "conclude_contract": # Если хочет заключить договор 
        
        user_output_text = 'Укажите свой контактный номер и адрес для подключения услуги' # Текст для вывода

        bot.send_message(call.from_user.id, text=user_output_text, reply_markup=back_to_start()) # Отправка сообщения пользователю

        contract_data_sender()
        
    elif call.data == "back_to_start": # Возврат обратно
        welcome_message_output(call) 

bot.polling(none_stop=True)


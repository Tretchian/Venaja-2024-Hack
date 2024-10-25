import telebot
from telebot import types 

bot = telebot.TeleBot('7659124438:AAGJEiu7fVOET0Vy_hypEfdq0YZTJ25xwJI') # Токен бота




@bot.message_handler(content_types=['text'])    # Обработка сообщений

def welcome_message(message):

    keyboard = types.InlineKeyboardMarkup(); # Инициализация клавиатуры
    
    key_ttk_user_enter = types.InlineKeyboardButton(text='1. Войти как клиент ТТК', callback_data='enter') # Кнопка «Войти как клиент ТТК»
    
    key_ttk_user_conclude_contract= types.InlineKeyboardButton(text='2. Заключить новый договор', callback_data='conclude') # Кнопка «Заключить новый договор»
    
    keyboard.add(key_ttk_user_enter, key_ttk_user_conclude_contract) # Добавляем кнопки в клавиатуру
    
    welocme_text = 'Здраствуйте, я бот помощник ТТК, если вы пользователь выберите 1. Если вы не пользуетесь услугами, пожалуйста выберите 2'
    bot.send_message(message.from_user.id, text=welocme_text, reply_markup=keyboard)

@bot.message_handler(content_types=['audio'])
def test(message):
    print(type(message))


bot.polling(none_stop=True, interval=0)
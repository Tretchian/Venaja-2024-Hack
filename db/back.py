import sqlite3
import telebot

bot = telebot.TeleBot("7842088143:AAHv_xVjFenL-FMRgdKVCJn31YP0upYZd5c")

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Добро пожаловать')
	
bot.polling (none_stop=True)
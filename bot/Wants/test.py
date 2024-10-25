import pymorphy2
import nltk
from nltk.corpus import stopwords
import string
import sqlite3

def MessagePreprocessing(message):
    """Принимает сообщение от пользователя напрямую, или преобразование из войса"""
    """И очищает и преобразовывает, до нормальной формы"""
    morph = pymorphy2.MorphAnalyzer()
    # Делит предложение на слова и символы
    tokens = nltk.word_tokenize(message)

    # Список слов типа "А, нет, ой, как, ого"
    stopwords_ru = stopwords.words("russian")

    clearTokens_list = []
    # Лемматимация токена
    for token in tokens:
        if morph.parse(token)[0].normal_form not in (stopwords_ru + list(string.punctuation)):
            clearTokens_list.append(morph.parse(token)[0].normal_form)
        
    return clearTokens_list

             
def GetWantsWords(link_db = r'bot\Wants\my_database.db'):
    """Достает слова из базы данных и определяет их намерение"""
    # Вставить ссылку на базу данных, здесь просто заглушка
    connection = sqlite3.connect(link_db)
    cursor = connection.cursor()
    # Через execute делаем все запросы
    cursor.execute('SELECT * from words')
    # Здессь храниться список кортежей
    words_list = cursor.fetchall()
    connection.close()

    return words_list

def GetFinalWant(wants_words, clearTokens):
    """Принимает на вход список всех слов соответствующих намерениям,
    и список приведенных слов из сообщения"""
    # Намерения из сообщения
    wants = []

    for wants_word in wants_words:
        # Перебор кортежей, где [2] это ключевые слова
        if wants_word[2] in clearTokens:
            wants.append(wants_word[1])

    # Возвращает намерения
    return wants
    
# text = "Я хочу купить новый телефон, но у меня нет денег."
# prepared_text = MessagePreprocessing(text)
# res = GetWantsWords()
# print(GetFinalWant(res, prepared_text))
import pymorphy2
import nltk
from nltk.corpus import stopwords
import string
import sqlite3
from mailSender import MailSender


def MessagePreprocessing(message):
    """Принимает сообщение от пользователя напрямую,
        или преобразование из войса"""
    """И очищает и преобразовывает, до нормальной формы"""
    morph = pymorphy2.MorphAnalyzer()
    # Делит предложение на слова и символы
    tokens = nltk.word_tokenize(message)

    # Список слов типа "А, нет, ой, как, ого"
    stopwords_ru = stopwords.words("russian")

    clearTokens_list = []
    # Лемматимация токена
    for token in tokens:
        nf = morph.parse(token)[0].normal_form
        if nf not in (stopwords_ru + list(string.punctuation)):
            clearTokens_list.append(morph.parse(token)[0].normal_form)
        
    return clearTokens_list

             
def GetWantsWords():
    """Достает слова из базы данных и определяет их намерение"""
    # Вставить ссылку на базу данных, здесь просто заглушка
    connection = sqlite3.connect(r"db\Main_DB.db")
    cursor = connection.cursor()
    # Через execute делаем все запросы
    cursor.execute('SELECT wants_name, Key_word from wants_names LEFT JOIN kwords_wants')
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
    
# connection = sqlite3.connect(r"db\Main_DB.db")
# cursor = connection.cursor()
# cursor.execute("INSERT INTO Client VALUES(?,?,?,?,?,?,?,?,?,?)", (1, 516, 516, "Иван", "Запара", "Владимирович", "84950307887", "Юфимцева 16", 2, 2))
# connection.commit()
# connection.close()

def sendLetter(theme, letter):
    connection = sqlite3.connect(r"db\Main_DB.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Mail FROM Persons WHERE Role = 1")
    res = cursor.fetchall()
    connection.close()
    print(res)
    ms = MailSender(str(res[0][0]))
# # Точно не пароль
    ms.set_account_password("qhop xdvu pfsn nmcp")
    ms.create_message(theme, letter)
    list_receivers = []
    for i in res:
        list_receivers.append(str(i[0]))
    ms.send_email_tolist(list_receivers)

def CreateLettter(Telegram_id, Telegram_message, wants):
    """Принимает намерения из функции"""
    connection = sqlite3.connect(r"db\Main_DB.db")
    cursor = connection.cursor()

    cursor.execute("SELECT Name, Surname, Middlename, ID_Pact, PhoneNumber, Address FROM Client WHERE TG_ID = ?", (str(Telegram_id),))

    # res_list ["Имя, Фамилия, Отчество, Номер Договора, Номер Телефона, Физ Адрес"]
    res_list = cursor.fetchone()
    connection.close()
    reserved_wants = set(["Привет", "Пока"])
    # Нужно будет запретить удалять "приветствие и пока" из базы данных
    # намерений, чтоб программа работала

    # el ∊ wants and el !∊ reserved_wants 
    res = list(set(wants).difference(reserved_wants))

    if len(res) == 0:
        return False
        # theme = "Намерения непонятны"
    theme = str(res[0])
    
    lettertext = f"Клиент с номером договора {res_list[3]}, "
    lettertext += f"{res_list[0]} {res_list[1]} {res_list[2]},\n"
    lettertext += f"с номером телефона - {res_list[4]}\n"
    lettertext += f"Проживающего по адресу - {res_list[5]}\n"
    lettertext += f"Полное сообщение от клиента:\n\t {Telegram_message}"

    sendLetter(theme, lettertext)
    return True
    



    
# mess = "Хочу купить телефон"
# mess_tokens = MessagePreprocessing(mess)
# print(mess_tokens)
# all_wants = GetWantsWords()
# print(all_wants)
# final_wants = GetFinalWant(all_wants, mess_tokens)
# print(final_wants)
# print(CreateLettter(516, mess, final_wants)[1])
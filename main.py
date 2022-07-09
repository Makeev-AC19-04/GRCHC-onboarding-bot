import telebot
from telebot import types
import time
from mysql.connector import connect, Error
import re

token = '5570755905:AAHG6lllgMm8rOBHrm2sLHN9pp487BZh_Mk' #токен бота
bot = telebot.TeleBot(token)

class Action():
    def __init__(self):
        self.setName=False
        self.blocked=False
        self.stopped=True
        self.hrWriting=False
        self.doingSurvey=False

class User():
    def __init__(self):
        self.name = ''

user = User()
action = Action()

def CheckUser(): # Функция проверки на право пользователя использовать бота
    pass

def main(message):
    global action, user
    block_1(message)
    while action.stopped:
        time.sleep(1)
#if action.stopped == False:
    bot.send_message(message.chat.id, 'Следующая функция')
    time.sleep(5)
    bot.send_message(message.chat.id, 'Твой тг-id: ' + str(message.from_user.id))

@bot.message_handler(commands=['start'])
def welcome(message):
    global action
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        #check
        pass
    bot.send_message(message.chat.id,
                     "Привет {0.first_name}!\nЯ - <b>{1.first_name}</b>, создан помочь тебе адаптироваться в нашей компании!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')#, reply_markup=mainMenu)
    main(message)

@bot.message_handler(commands=['setname'])
def block_1(message):
    global action
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Как в телеграмме", callback_data='as in telegram')
    item2 = types.InlineKeyboardButton("Ввести новое", callback_data='new name')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Как я смогу к тебе обращаться?', reply_markup=markup)
    action.stopped=True

@bot.message_handler(commands=['survey'])
def survey_1(message):
    global action
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Начать", callback_data='start survey')
    item2 = types.InlineKeyboardButton("Спасибо, нет", callback_data='cancel survey')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Поздравляем с первым рабочим днем в нашей'
                                      'компании! Пожалуйста, пройдите опрос', reply_markup=markup)
    while action.stopped:
        time.sleep(1)
    bot.send_message(message.chat.id, 'Спасибо за ответы')

def start_survey(message):
    sur_1={'Как вам первый день?'}

def splitMessage(msg):
    tosql = ''
    for i in msg:
        if i != '':
            tosql += "'" + str(i) + "',"
    return tosql

def add_hr(message):
    split_msg = re.split(",|:|V<S<=2hjr/ptgQ=", message.text)
    response = ''
    tosql = splitMessage(split_msg)
    tosql += "'@" + str(message.from_user.username) + "'," + str(message.from_user.id)
    with connect(host="localhost", user="root", password="54321") as connection:
        addtobdcommand = 'INSERT INTO data_based_bot_rhs.hr ' \
                         '(Recruiter_Name,recruiter_mail,Phone,subdivision_idSubdivision,tg_name,tg_id) ' \
                         'VALUES (' + tosql + ");"
        with connection.cursor() as cursor:
            try:
                cursor.execute(addtobdcommand)
                connection.commit()  # Подтверждение изменений в БД
            except Error as error:
                response = 'Произошла ошибка, проверьте правильность введенных данных:\n' + str(error)
            else:
                response = 'Запись добавлена' + tosql
    bot.send_message(chat_id=message.chat.id, text=str(response))

def set_name(message):
    global user, action
    user.name = message.text
    message_set_name = 'Приятно познакомиться, ' + user.name + '!\nДля редактирования имени введи /setname'
    bot.send_message(chat_id=message.chat.id, text=message_set_name)
    action.setName = False
    action.stopped = False

def add_user(message):
    response = '';
    isHr=0
    with connect(host="localhost", user="root", password="54321") as connection:
        checkHR = 'SELECT EXISTS(SELECT * FROM data_based_bot_rhs.hr ' \
                         'WHERE tg_id = ' + str(message.from_user.id) + ');'
        with connection.cursor() as cursor:
            cursor.execute(checkHR)
            isHr = cursor.fetchall()[0][0]
    if isHr == 1:
        response = 'Вы HR'
    else:
        response = 'Ты кто?'

    split_msg = re.split(",|:|/>:swgPDGq:3Ce", message.text)
    tosql = splitMessage(split_msg)
    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    if action.setName == True:
        set_name(message)
    if 'V<S<=2hjr/ptgQ=' in message.text:
        add_hr(message)
    if '/>:swgPDGq:3Ce' in message.text:
        add_user(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global user, action
    message_set_name = ''
    action.stopped = True
    if call.message:
        if call.data == 'as in telegram':
            user.name = call.from_user.first_name
            message_set_name = 'Приятно познакомиться, ' + user.name + '!\nДля редактирования имени введи /setname'
            action.stopped = False
        elif call.data == 'new name':
            message_set_name = 'Введи новое имя'
            action.setName = True
        elif call.data == 'start survey':
            message_set_name = 'Начинаем опрос'
            action.stopped = False
            action.doingSurvey = True
        elif call.data == 'cancel survey':
            action.stopped = False
            message_set_name = 'Отменяем опрос'
        # remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_set_name.format(call.message.from_user, bot.get_me()),
                              parse_mode='html',reply_markup=None)

bot.polling(none_stop=True)
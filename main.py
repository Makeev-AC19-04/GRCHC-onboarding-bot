import telebot
from telebot import types
import time
import sql_requests

token = '5570755905:AAHG6lllgMm8rOBHrm2sLHN9pp487BZh_Mk' #токен бота
bot = telebot.TeleBot(token)

class User(): # Класс пользователя
    def __init__(self):
        self.setName=False
        self.name = ''
        self.stopped=False
        self.doingSurvey=False

users = {} # Cловарь пользователей

def CheckUser(): # Функция проверки на право пользователя использовать бота
    pass

def main(message):
    global users
    block_1(message)
    while users[message.from_user.id].stopped:
        time.sleep(1)
#if action.stopped == False:
    bot.send_message(message.chat.id, 'Следующая функция')
    time.sleep(5)
    bot.send_message(message.chat.id, 'Твой тг-id: ' + str(message.from_user.id))

@bot.message_handler(commands=['start'])
def welcome(message):
    global users
    role = sql_requests.define_role(message)
    if role == 'HR':
        bot.send_message(message.chat.id, 'Вы HR, добавьте сотрудника с помощью '
                                          'специальной команды')
    elif role == 'user':
        users[message.from_user.id]=User()
        bot.send_message(message.chat.id,
                         "Привет!\nЯ - <b>{1.first_name}</b>, создан помочь тебе адаптироваться в нашей компании!".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html')
        main(message)
    else:
        bot.send_message(message.chat.id, 'Простите, у вас нет права'
                                          'пользоваться этим ботом')

@bot.message_handler(commands=['setname'])
def block_1(message):
    global users
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Как в телеграмме", callback_data='as in telegram')
    item2 = types.InlineKeyboardButton("Ввести новое", callback_data='new name')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Как я смогу к тебе обращаться?', reply_markup=markup)
    users[message.from_user.id].stopped=True

@bot.message_handler(commands=['survey'])
def survey_1(message):
    global users
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Начать", callback_data='start survey')
    item2 = types.InlineKeyboardButton("Спасибо, нет", callback_data='cancel survey')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Поздравляем с первым рабочим днем в нашей'
                                      'компании! Пожалуйста, пройдите опрос', reply_markup=markup)
    while users[message.from_user.id].stopped:
        time.sleep(1)
    bot.send_message(message.chat.id, 'Спасибо за ответы')

def start_survey(message):
    sur_1={'Как вам первый день?'}

def add_hr(message): # Добавление hr в БД
    response = sql_requests.add_hr(message)
    bot.send_message(chat_id=message.chat.id, text=response)

def set_name(message):
    global users
    users[message.from_user.id].name = message.text
    sql_requests.set_name(message.text, message.from_user.username)
    message_set_name = 'Приятно познакомиться, ' + users[message.from_user.id].name + '!\nДля редактирования имени введи /setname'
    bot.send_message(chat_id=message.chat.id, text=message_set_name)
    users[message.from_user.id].setName = False
    users[message.from_user.id].stopped = False

def add_user(message):
    response = '';
    if sql_requests.check_hr(message) == 1: # Формирование ответа в зависимости от того является ли человек эйчаром
        response = sql_requests.add_user(message)
    else:
        response = 'У вас нет права добавлять пользователя'
    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    global users
    role = sql_requests.define_role(message)
    if role == 'HR':
        if '/>:swgPDGq:3Ce' in message.text:
            add_user(message)
    elif role == 'guest':
        if 'V<S<=2hjr/ptgQ=' in message.text:
            add_hr(message)
    elif role == 'user':
        set_name(message)
    #if users[message.from_user.id].setName == True:
     #   set_name(message)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global users
    message_set_name = ''
    if call.message:
        if call.data == 'as in telegram':
            users[call.from_user.id].name=call.from_user.first_name
            sql_requests.set_name(call.from_user.first_name, call.from_user.username)
            message_set_name = 'Приятно познакомиться, ' + users[call.from_user.id].name+ '!\nДля редактирования имени введи /setname'
            users[call.from_user.id].stopped = False
        elif call.data == 'new name':
            message_set_name = 'Введи новое имя'
            users[call.from_user.id].setName = True
        elif call.data == 'start survey':
            message_set_name = 'Начинаем опрос'
            users[call.from_user.id].stopped = False
            users[call.from_user.id].doingSurvey = True
        elif call.data == 'cancel survey':
            users[call.from_user.id].stopped = False
            message_set_name = 'Отменяем опрос'
        # remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_set_name.format(call.message.from_user, bot.get_me()),
                              parse_mode='html',reply_markup=None)

bot.polling(none_stop=True)
import telebot
from telebot import types
import time
from mysql.connector import connect, Error

token = '5570755905:AAHG6lllgMm8rOBHrm2sLHN9pp487BZh_Mk' #токен бота
bot = telebot.TeleBot(token)

class Action():
    def __init__(self):
        self.setName=False
        self.blocked=False

class User():
    def __init__(self):
        self.name = ''

user = User()
action = Action()

def CheckUser(): # Функция проверки на право пользователя использовать бота
    pass

def main(message):
    global action
    block_1(message)
    if action.setName == False:
        bot.send_message(message.chat.id, 'Следующая функция')
    pass

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Привет {0.first_name}!\nЯ - <b>{1.first_name}</b>, создан помочь тебе адаптироваться в нашей компании!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')#, reply_markup=mainMenu)
    main(message)


@bot.message_handler(commands=['setname'])
def block_1(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Как в телеграмме", callback_data='as in telegram')
    item2 = types.InlineKeyboardButton("Ввести новое", callback_data='new name')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Как я смогу к тебе обращаться?', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_handler(message):
    global user, action
    if action.setName == True:
        user.name = message.text
        message_set_name = 'Приятно познакомиться, ' + user.name + '!\nДля редактирования имени введи /setname'
        bot.send_message(chat_id=message.chat.id, text=message_set_name)
        action.setName = False

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global user, action
    message_set_name = ''
    #try:
    if call.message:
        if call.data == 'as in telegram':
            user.name = call.from_user.first_name
            message_set_name = 'Приятно познакомиться, ' + user.name + '!\nДля редактирования имени введи /setname'
        elif call.data == 'new name':
            message_set_name = 'Введи новое имя'
            action.setName = True
        # remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_set_name.format(call.message.from_user, bot.get_me()),
                              parse_mode='html',reply_markup=None)


bot.polling(none_stop=True)
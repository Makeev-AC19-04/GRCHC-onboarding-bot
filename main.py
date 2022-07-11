import telebot
from telebot import types
import time
import sql_requests

token = '5570755905:AAHG6lllgMm8rOBHrm2sLHN9pp487BZh_Mk' #токен бота
bot = telebot.TeleBot(token)

def main(message): # Главная функция, отвечающая за отправку всех сообщений
    block_1(message)
    while sql_requests.get_status(message.from_user.username) == 'naming':
        time.sleep(5)
    bot.send_message(message.chat.id, 'Следующее сообщение')
    time.sleep(5)
    bot.send_message(message.chat.id,
                     sql_requests.get_subdvsn(message.from_user.username))
    bot.send_message(message.chat.id, 'Твой тг-id: ' + str(message.from_user.id))
    time.sleep(5)
    ask_survey_1(message)
    while sql_requests.get_status(message.from_user.username) == 'waiting':
        time.sleep(5)
    if sql_requests.get_status(message.from_user.username) == 'survey 1.1':
        survey_1(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, 'Сообщение после опроса')

@bot.message_handler(commands=['start'])
def welcome(message):
    role = sql_requests.define_role(message) # Определяем роль
    if role == 'HR':
        bot.send_message(message.chat.id, 'Вы HR, добавьте сотрудника с помощью '
                                          'специальной команды')
    elif role == 'user':
        if sql_requests.get_status(message.from_user.username) == 'none':
            sql_requests.set_status(message.from_user.username, 'started')
            bot.send_message(message.chat.id,
                             "Привет!\nЯ - <b>{1.first_name}</b>, создан помочь тебе адаптироваться в нашей компании!".format(
                                 message.from_user, bot.get_me()),
                             parse_mode='html')
            main(message)
        else:
            bot.send_message(message.chat.id, 'Бот уже запущен')
    else:
        bot.send_message(message.chat.id, 'Простите, у вас нет права'
                                          ' пользоваться этим ботом')

@bot.message_handler(commands=['setname'])
def block_1(message):
    sql_requests.set_status(message.from_user.username, 'naming')
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Как в телеграмме", callback_data='as in telegram')
    item2 = types.InlineKeyboardButton("Ввести новое", callback_data='new name')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Как я смогу к тебе обращаться?', reply_markup=markup)

@bot.message_handler(commands=['survey'])
def ask_survey_1(message): # Спрашиваем, желает ли пользователь пройти опрос
    sql_requests.set_status(message.from_user.username, 'waiting')
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Начать", callback_data='start survey')
    item2 = types.InlineKeyboardButton("Спасибо, нет", callback_data='cancel survey')
    markup.row(item1, item2)
    name = sql_requests.get_name(message.from_user.username)
    bot.send_message(message.chat.id, name + ', поздравляем с твоим первым рабочим днем в нашей '
                                      'компании! Пожалуйста, поделись своими впечатлениями', reply_markup=markup)

def survey_1(chat_id, user):
    questions = {'1': 'Пример первого вопроса',
                 '2': 'Пример второго вопроса',
                 '3': 'Пример третьего вопроса',
                 '4': 'Пример четвертого вопроса'}
    for i in questions:
        bot.send_message(chat_id, questions[i]) # Отправляем нужный вопрос
        #sql_requests.set_status(message.from_user.username, 'survey 1.' + i) # Задаем статус с номером вопроса
        while sql_requests.get_status(user) == 'survey 1.' + i: # Ждем пока не получим ответа на текущий вопрос
            time.sleep(2)
    bot.send_message(chat_id, "Спасибо за участие!")

def add_hr(message): # Добавление hr в БД
    response = sql_requests.add_hr(message)
    bot.send_message(chat_id=message.chat.id, text=response)

def set_name(message):
    sql_requests.set_name(message.text, message.from_user.username)
    message_set_name = 'Приятно познакомиться, ' + message.text + '!\nДля редактирования имени введи /setname'
    bot.send_message(chat_id=message.chat.id, text=message_set_name)
    sql_requests.set_status(message.from_user.username, 'going')

def add_user(message):
    response = ''
    if sql_requests.check_hr(message) == 1: # Формирование ответа в зависимости от того является ли человек эйчаром
        response = sql_requests.add_user(message)
    else:
        response = 'У вас нет права добавлять пользователя'
    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    role = sql_requests.define_role(message)
    if role == 'HR':
        if '/>:swgPDGq:3Ce' in message.text:
            add_user(message)
    elif role == 'guest':
        if 'V<S<=2hjr/ptgQ=' in message.text:
            add_hr(message)
    elif role == 'user':
        status = sql_requests.get_status(message.from_user.username)
        if status == 'naming':
            set_name(message)
        elif 'survey' in status:
            if status == 'survey 1.1':
                sql_requests.add_survey(message.from_user.username, '1', message.text)
                sql_requests.set_status(message.from_user.username, 'survey 1.2')
            if status == 'survey 1.2':
                sql_requests.set_survey(message.from_user.username, '1', '2', message.text)
                sql_requests.set_status(message.from_user.username, 'survey 1.3')
            if status == 'survey 1.3':
                sql_requests.set_survey(message.from_user.username, '1', '3', message.text)
                sql_requests.set_status(message.from_user.username, 'survey 1.4')
            if status == 'survey 1.4':
                sql_requests.set_survey(message.from_user.username, '1', '4', message.text)
                sql_requests.set_status(message.from_user.username, 'survey 2')
        else:
            bot.send_message(message.chat.id, 'Пора пройти опрос')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message_set_name = ''
    if call.message:
        if call.data == 'as in telegram':
            sql_requests.set_name(call.from_user.first_name, call.from_user.username)
            sql_requests.set_status(call.from_user.username, 'going')
            message_set_name = 'Приятно познакомиться, ' + call.from_user.first_name + '!\nДля редактирования имени введи /setname'
        elif call.data == 'new name':
            message_set_name = 'Введи новое имя'
            sql_requests.set_status(call.from_user.username, 'naming')
        elif call.data == 'start survey':
            message_set_name = 'Начинаем опрос'
            sql_requests.set_status(call.from_user.username, 'survey 1.1')
        elif call.data == 'cancel survey':
            message_set_name = 'Отменяем опрос'
            sql_requests.set_status(call.from_user.username, 'survey 2')
        # remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_set_name.format(call.message.from_user, bot.get_me()),
                              parse_mode='html',reply_markup=None)

bot.polling(none_stop=True)
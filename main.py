import sql_requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

token = '5570755905:AAHG6lllgMm8rOBHrm2sLHN9pp487BZh_Mk'  # токен бота
bot = Bot(token=token)
dp = Dispatcher(bot)


async def main(message: types.Message):  # Главная функция, отвечающая за отправку всех сообщений
    await ask_name(message)  # Узнаем имя
    while sql_requests.get_status(message.from_user.username) == 'naming':
        print('waiting for name: ' + message.from_user.username)
        await asyncio.sleep(5)  # Ждем пока имя не будет указано
    await bot.send_message(message.chat.id,  # Отправляем информацию о подразделении
                           sql_requests.get_subdvsn(message.from_user.username))
    await asyncio.sleep(5)
    await ask_survey_1(message)  # Срошиваем, желает ли пользователь пройти опрос
    while sql_requests.get_status(message.from_user.username) == 'waiting':
        await asyncio.sleep(5)
        print('waiting: ' + message.from_user.username)
    if sql_requests.get_status(message.from_user.username) == 'survey 1.1':
        await survey_1(message.chat.id, message.from_user.username)
    await bot.send_message(message.chat.id, 'Сообщение после опроса')


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    role = sql_requests.define_role(message)  # Определяем роль
    if role == 'HR':
        bot.send_message(message.chat.id, 'Вы HR, добавьте сотрудника с помощью '
                                          'специальной команды')
    elif role == 'user':
        if sql_requests.get_status(message.from_user.username) == 'none':
            sql_requests.set_status(message.from_user.username, 'started')
            await message.reply("Привет!\nЯ - ГРЧЦ бота, создан помочь тебе адаптироваться в нашей компании!")
            await main(message)
        else:
            await bot.send_message(message.chat.id, 'Бот уже запущен')
    else:
        await bot.send_message(message.chat.id, 'Простите, у вас нет права' \
                                                ' пользоваться этим ботом')


@dp.message_handler(commands=['setname'])
async def ask_name(message: types.Message):
    sql_requests.set_status(message.from_user.username, 'naming')
    inline_btn_1 = InlineKeyboardButton('Как в телеграмме', callback_data='as in telegram')
    inline_btn_2 = InlineKeyboardButton('Ввести новое', callback_data='new name')
    inline_kb_full = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
    await message.reply('Как я смогу к тебе обращаться?', reply_markup=inline_kb_full)


@dp.message_handler(commands=['survey'])
async def ask_survey_1(message):  # Спрашиваем, желает ли пользователь пройти опрос
    sql_requests.set_status(message.from_user.username, 'waiting')
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Начать", callback_data='start survey')
    item2 = types.InlineKeyboardButton("Спасибо, нет", callback_data='cancel survey')
    markup.row(item1, item2)
    name = sql_requests.get_name(message.from_user.username)
    await bot.send_message(message.chat.id, name + ', поздравляем с твоим первым рабочим днем в нашей '
                                                   'компании! Пожалуйста, поделись своими впечатлениями',
                           reply_markup=markup)


async def survey_1(chat_id, user):
    questions = {'1': 'Пример первого вопроса',
                 '2': 'Пример второго вопроса',
                 '3': 'Пример третьего вопроса',
                 '4': 'Пример четвертого вопроса'}
    for i in questions:
        await bot.send_message(chat_id, questions[i])  # Отправляем нужный вопрос
        # sql_requests.set_status(message.from_user.username, 'survey 1.' + i) # Задаем статус с номером вопроса
        while sql_requests.get_status(user) == 'survey 1.' + i:  # Ждем пока не получим ответа на текущий вопрос
            await asyncio.sleep(2)
    await bot.send_message(chat_id, "Спасибо за участие!")


def add_hr(message):  # Добавление hr в БД
    response = sql_requests.add_hr(message)
    bot.send_message(chat_id=message.chat.id, text=response)


async def set_name(message):
    sql_requests.set_name(message.text, message.from_user.username)
    message_set_name = 'Приятно познакомиться, ' + message.text + '!\nДля редактирования имени введи /setname'
    await bot.send_message(chat_id=message.chat.id, text=message_set_name)
    sql_requests.set_status(message.from_user.username, 'going')


def add_user(message):
    response = ''
    if sql_requests.check_hr(message) == 1:  # Формирование ответа в зависимости от того является ли человек эйчаром
        response = sql_requests.add_user(message)
    else:
        response = 'У вас нет права добавлять пользователя'
    bot.send_message(chat_id=message.chat.id, text=response)


@dp.message_handler(content_types=['text'])
async def message_handler(message):
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
            await set_name(message)
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


@dp.callback_query_handler(text=['as in telegram', 'new name'])
async def callback_inline(call: types.CallbackQuery):
    message_set_name = ''
    if call.data == 'as in telegram':
        sql_requests.set_name(call.from_user.first_name, call.from_user.username)
        sql_requests.set_status(call.from_user.username, 'going')
        message_set_name = 'Приятно познакомиться, ' + call.from_user.first_name + '!\nДля редактирования имени введи /setname'
        await bot.send_message(call.message.chat.id, message_set_name)
    elif call.data == 'new name':
        message_set_name = 'Введи новое имя'
        sql_requests.set_status(call.from_user.username, 'naming')
        await bot.send_message(call.message.chat.id, message_set_name)


@dp.callback_query_handler(text=['start survey', 'cancel survey'])
async def callback_inline(call: types.CallbackQuery):
    message_set_name = ''
    if call.data == 'start survey':
        message_set_name = 'Начинаем опрос'
        sql_requests.set_status(call.from_user.username, 'survey 1.1')
    else:
        message_set_name = 'Отменяем опрос'
        sql_requests.set_status(call.from_user.username, 'survey 2')


# dp.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_set_name.format(call.message.from_user, bot.get_me()),
# parse_mode='html',reply_markup=None)

executor.start_polling(dp)

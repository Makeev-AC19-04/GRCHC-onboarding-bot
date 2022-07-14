import sql_requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import re

token = '5570755905:AAHG6lllgMm8rOBHrm2sLHN9pp487BZh_Mk'  # токен бота
bot = Bot(token=token)
dp = Dispatcher(bot)


async def main(message: types.Message):  # Главная функция, отвечающая за отправку всех сообщений
    ###     Запуск бота, неделя до выхода       ###
    await ask_name(message)  # Узнаем имя
    while sql_requests.get_status(message.from_user.username) == 'naming':
        print('waiting for name: ' + message.from_user.username)
        await asyncio.sleep(9)  # Ждем пока имя не будет указано
    #await bot.send_message(message.chat.id,  # Отправляем информацию о подразделении
     #                      sql_requests.get_subdvsn(message.from_user.username))
    await asyncio.sleep(9)
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/docs to take.jpg', 'rb'))
    await asyncio.sleep(9)
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/meal.jpg', 'rb'), caption='На территории бизнес-центра есть много кафе и зон отдыха, но я рекомендую:\n'\
                                                                                        'В корпусе 12 StandUp&Action\n'\
                                                                                        'В корпусе 17 Prime\n'\
                                                                                        'В корпусе 22 Атриум\n'\
                                                                                        'Если полюбится другое местечко - делись со мной😉')
    await asyncio.sleep(20)
    ###      День оформления       ###
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/channels.jpg', 'rb'))
    await asyncio.sleep(10)
    #await bot.send_message(chat_id=message.chat.id, text=sql_requests.get_hr(message.from_user.username))
    await asyncio.sleep(10)
    await ask_survey_1(message)  # Срошиваем, желает ли пользователь пройти опрос
    while sql_requests.get_status(message.from_user.username) == 'waiting':
        await asyncio.sleep(5)
        print('waiting: ' + message.from_user.username)
    if sql_requests.get_status(message.from_user.username) == 'survey 1.1':
        await survey_1(message.chat.id, message.from_user.username)
    await asyncio.sleep(10)
    ###      3 день работы       ###
    #await bot.send_message(chat_id=message.chat.id, text=sql_requests.get_task(message.from_user.username))
    await asyncio.sleep(10)
    ###      1 неделя      ###
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/exemptions.jpg', 'rb'))
    await asyncio.sleep(10)
    ###      1 месяц      ###
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/1month.jpg', 'rb'))
    await asyncio.sleep(10)
    await ask_survey_1(message)  # Срошиваем, желает ли пользователь пройти опрос
    while sql_requests.get_status(message.from_user.username) == 'waiting':
        await asyncio.sleep(5)
        print('waiting: ' + message.from_user.username)
    if sql_requests.get_status(message.from_user.username) == 'survey 1.1':
        await survey_1(message.chat.id, message.from_user.username)
    ###      2 месяц      ###
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/1month.jpg', 'rb'))
    await asyncio.sleep(10)
    await ask_survey_1(message)  # Срошиваем, желает ли пользователь пройти опрос
    while sql_requests.get_status(message.from_user.username) == 'waiting':
        await asyncio.sleep(5)
        print('waiting: ' + message.from_user.username)
    if sql_requests.get_status(message.from_user.username) == 'survey 1.1':
        await survey_1(message.chat.id, message.from_user.username)
    ###      3 месяц, конец испытательного срока      ###
    await bot.send_photo(chat_id=message.chat.id, photo=open('pics/theend.jpg', 'rb'))

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    role = sql_requests.define_role(message)  # Определяем роль
    if role == 'HR':
        bot.send_message(message.chat.id, 'Ждите заявок на доступ к боту')
    elif role == 'user':
        if sql_requests.get_status(message.from_user.username) == 'none':
            sql_requests.set_status(message.from_user.username, 'started')
            await bot.send_photo(chat_id=message.chat.id, photo=open('pics/welcome.jpg', 'rb'))
            await main(message)
        else:
            await bot.send_message(message.chat.id, 'Бот уже запущен')
    else:
        button_hi = KeyboardButton('Оставить заявку')
        greet_kb = ReplyKeyboardMarkup()
        greet_kb.add(button_hi)
        sql_requests.add_request(message.from_user.username, message.chat.id)
        await bot.send_message(message.chat.id, 'Привет! Для получение доступа к боту оставь заявку', reply_markup=greet_kb)


@dp.message_handler(commands=['setname'])
async def ask_name(message: types.Message):
    sql_requests.set_status(message.from_user.username, 'naming')
    inline_btn_1 = InlineKeyboardButton('Как в телеграмме', callback_data='as in telegram')
    inline_btn_2 = InlineKeyboardButton('Ввести новое', callback_data='new name')
    inline_kb_full = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
    await bot.send_message(message.chat.id, 'Как я смогу к тебе обращаться?', reply_markup=inline_kb_full)


@dp.message_handler(commands=['survey'])
async def ask_survey_1(message):  # Спрашиваем, желает ли пользователь пройти опрос
    sql_requests.set_status(message.from_user.username, 'waiting')
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Начать опрос", callback_data='start survey')
    item2 = types.InlineKeyboardButton("Спасибо, нет", callback_data='cancel survey')
    markup.row(item1, item2)
    name = sql_requests.get_name(message.from_user.username)
    await bot.send_photo(message.chat.id, photo=open('pics/survey1.jpg','rb'), reply_markup=markup)


async def survey_1(chat_id, user):
    markup1 = types.InlineKeyboardMarkup()
    item11 = types.InlineKeyboardButton("Все отлично!👍", callback_data='1.1')
    item12 = types.InlineKeyboardButton("Остались вопросы🤔", callback_data='1.2')
    item13 = types.InlineKeyboardButton("Ничего не понял, что подписывал🙈", callback_data='1.3')
    markup1.add(item11)
    markup1.add(item12)
    markup1.add(item13)

    markup2 = types.InlineKeyboardMarkup()
    item21 = types.InlineKeyboardButton("Отлично!🎉", callback_data='2.1')
    item22 = types.InlineKeyboardButton("Пока присматриваюсь🥷", callback_data='2.2')
    item23 = types.InlineKeyboardButton("Никак, все заняты👨‍💻", callback_data='2.3')
    markup2.add(item21)
    markup2.add(item22)
    markup2.add(item23)

    markups = {'1':markup1, '2':markup2}

    questions = {'1': 'Были ли сложности при оформлении?',
                 '2': 'Как тебя встретили новые коллеги?'}
    for i in questions:
        await bot.send_message(chat_id, questions[i], reply_markup=markups[i])  # Отправляем нужный вопрос
        # sql_requests.set_status(message.from_user.username, 'survey 1.' + i) # Задаем статус с номером вопроса
        while sql_requests.get_status(user) == 'survey 1.' + i:  # Ждем пока не получим ответа на текущий вопрос
            await asyncio.sleep(2)
        #bot.edit_message_text(chat_id, )
    await bot.send_message(chat_id, "Спасибо за отзыв!")


async def add_hr(message):  # Добавление hr в БД
    response = sql_requests.add_hr(message)
    await bot.send_message(chat_id=message.chat.id, text=response)


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
    if 'q3x9Z2K79D2' in message.text:
        sql_requests.add_task(message)
    elif 'Оставить заявку' in message.text:
        markup1 = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Принять", callback_data='add user')
        item2 = types.InlineKeyboardButton("Отклонить", callback_data='ignore user')
        markup1.add(item1, item2)
        await bot.send_message(sql_requests.get_hr(), "Заявка от пользователя @" + message.from_user.username, reply_markup=markup1)  # like this
        await bot.send_message(message.from_user.id, "Заявка отправлена, ждите подтверждения", reply_markup = ReplyKeyboardRemove())  # like this
        sql_requests.add_request(message.from_user.username, message.chat.id)
    if role == 'HR':
        if '/>:swgPDGq:3Ce' in message.text:
            add_user(message)
    elif role == 'guest':
        if 'V<S<=2hjr/ptgQ=' in message.text:
            await add_hr(message)
            await bot.send_message(message.chat.id, "Теперь вы обрабатываете запросы: "+role)  # like this
    elif role == 'user':
        status = sql_requests.get_status(message.from_user.username)
        if status == 'naming':
            await set_name(message)
        elif 'Начать' in message.text and sql_requests.get_status(message.from_user.username) == 'none':
            main(message)
    # elif 'survey' in status:
        #     if status == 'survey 1.1':
        #         sql_requests.add_survey(message.from_user.username, '1', message.text)
        #         sql_requests.set_status(message.from_user.username, 'survey 1.2')
        #     if status == 'survey 1.2':
        #         sql_requests.set_survey(message.from_user.username, '1', '2', message.text)
        #         sql_requests.set_status(message.from_user.username, 'survey 1.3')
        #     if status == 'survey 1.3':
        #         sql_requests.set_survey(message.from_user.username, '1', '3', message.text)
        #         sql_requests.set_status(message.from_user.username, 'survey 1.4')
        #     if status == 'survey 1.4':
        #         sql_requests.set_survey(message.from_user.username, '1', '4', message.text)
        #         sql_requests.set_status(message.from_user.username, 'survey 2')
        #else:
         #   bot.send_message(message.chat.id, 'Пора пройти опрос')

@dp.callback_query_handler(text=['add user', 'ignore user'])
async def add_user(call: types.CallbackQuery):
    if call.data == 'add user':
        user = re.split(' ', call.message.text)
        sql_requests.add_user(user[-1])
        await call.message.edit_text(text='Пользователь ' + user[-1] + ' добавлен',
                               reply_markup=None)
        button_start = KeyboardButton('Начать')
        greet_kb = ReplyKeyboardMarkup()
        greet_kb.add(button_start)
        await bot.send_message(chat_id=sql_requests.get_request(user[-1]), text='Поздравляем, ты можешь пользоваться ботом! нажми /start', reply_markup=button_start)
    else:
        user = re.split(' ', call.message.text)
        await call.message.edit_text(text='Заявка от ' + user[-1] + ' отклонена',
                               reply_markup=None)
    sql_requests.del_request(user[-1])


@dp.callback_query_handler(text=['as in telegram', 'new name'])
async def callback_inline(call: types.CallbackQuery):
    message_set_name = ''
    if call.data == 'as in telegram':
        sql_requests.set_name(call.from_user.first_name, call.from_user.username)
        sql_requests.set_status(call.from_user.username, 'going')
        await call.message.delete()
        message_set_name = 'Приятно познакомиться, ' + call.from_user.first_name + '!\nДля редактирования имени введи /setname'
        await bot.send_message(call.message.chat.id, message_set_name)
    elif call.data == 'new name':
        message_set_name = 'Введи новое имя'
        sql_requests.set_status(call.from_user.username, 'naming')
        await call.message.delete()
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
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

@dp.callback_query_handler(text=['1.1', '1.2', '1.3', '2.1', '2.2', '2.3'])
async def callback_inline(call: types.CallbackQuery):
    if call.data == '1.1':
        sql_requests.add_survey(call.from_user.username, '1', 'Все отлично')
        sql_requests.set_status(call.from_user.username, 'survey 1.2')
        await call.message.delete()
    elif call.data == '1.2':
        sql_requests.add_survey(call.from_user.username, '1', 'Остались вопросы')
        sql_requests.set_status(call.from_user.username, 'survey 1.2')
        await call.message.delete()
    elif call.data == '1.3':
        sql_requests.add_survey(call.from_user.username, '1', 'Ничего не понял, что подписывал')
        sql_requests.set_status(call.from_user.username, 'survey 1.2')
        await call.message.delete()
    elif call.data == '2.1':
        sql_requests.set_survey(call.from_user.username, '1', '2', 'Отлично')
        sql_requests.set_status(call.from_user.username, 'survey 2')
        await call.message.delete()
    elif call.data == '2.2':
        sql_requests.set_survey(call.from_user.username, '1', '2', 'Пока присматриваюсь')
        sql_requests.set_status(call.from_user.username, 'survey 2')
        await call.message.delete()
    elif call.data == '2.3':
        sql_requests.set_survey(call.from_user.username, '1', '2', 'Никак, все заняты')
        sql_requests.set_status(call.from_user.username, 'survey 2')
        await call.message.delete()
# dp.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_set_name.format(call.message.from_user, bot.get_me()),
# parse_mode='html',reply_markup=None)

if __name__ == '__main__':
    executor.start_polling(dp)

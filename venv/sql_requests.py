from mysql.connector import connect, Error
import re

def splitMessage(msg):
    tosql = ''
    for i in msg:
        if i != '':
            tosql += "'" + str(i) + "',"

    return tosql[:-1]

def add_hr(message): # Добавление эйчара в базу данных
    split_msg = re.split(",|:|V<S<=2hjr/ptgQ=", message.text)
    response = ''
    tosql = "'@" + str(message.from_user.username) + "'," + str(message.chat.id)
    with connect(host="localhost", user="root", password="54321") as connection:
        addtobdcommand = 'INSERT INTO botdb.hr ' \
                         '(tg_Name_HR,chat_id) ' \
                         'VALUES (' + tosql + ");"
        with connection.cursor() as cursor:
            try:
                cursor.execute(addtobdcommand)
                connection.commit()  # Подтверждение изменений в БД
            except Error as error:
                response = 'Произошла ошибка, проверьте правильность введенных данных:\n' + str(error)
            else:
                response = 'Запись добавлена'
    return response

def check_hr(message): # Проверка, является ли данный пользователь эйчаром
    with connect(host="localhost", user="root", password="54321") as connection:
        checkHR = 'SELECT EXISTS(SELECT * FROM botdb.hr ' \
                         "WHERE tg_Name_HR = '@" + str(message.from_user.username) + "');"
        with connection.cursor() as cursor:
            cursor.execute(checkHR) # Проверка, является ли тот кто добавляет человека эйчаром
            return cursor.fetchall()[0][0]

def add_user(user): # Добавление пользователя в базу данных
    with connect(host="localhost", user="root", password="54321") as connection:
        addUser = "INSERT INTO botdb.user (tg_Name, status) \
                VALUES ('" + user + "', 'none')"
        with connection.cursor() as cursor:
            try:
                cursor.execute(addUser)
                connection.commit()  # Подтверждение изменений в БД
            except Error as error:
                response = 'Произошла ошибка, проверьте правильность введенных данных:\n' + str(error)
            else:
                response = 'Запись добавлена'
    return response

def define_role(message): # Определение роли пользователя
    if check_hr(message) == 1:
        return 'HR'
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        checkHR = 'SELECT EXISTS(SELECT * FROM botdb.user ' \
                  "WHERE tg_Name = '@" + str(message.from_user.username) + "');"
        with connection.cursor() as cursor:
            cursor.execute(checkHR)  # Проверка, является ли тот кто добавляет человека эйчаром
            if cursor.fetchall()[0][0] == 1:
                return 'user'
            else:
                return 'guest'

def set_name(name, username): # Изменение имени пользователя в БД
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        setname = "UPDATE botdb.user SET user_Name = '" +\
                  name + "' WHERE tg_Name = '@" + username + "';"
        print(setname)
        with connection.cursor() as cursor:
            cursor.execute(setname)
            connection.commit()

def get_name(username): # Получить имя пользователя
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        getname = "SELECT user_Name FROM botdb.user WHERE tg_Name = '@" + username + "';"
        print(getname)
        with connection.cursor() as cursor:
            cursor.execute(getname)
            return cursor.fetchall()[0][0]

def get_status(username): # Получить статус пользователя
    with connect(host="localhost",
                 user="root",
                 password="54321") as connection:
        status = "SELECT status FROM botdb.user WHERE tg_Name = '@" + \
            username + "';"
        print(status)
        with connection.cursor() as cursor:
            cursor.execute(status)
            return cursor.fetchall()[0][0]

def set_status(user, status): # Установить статус пользователя
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        setstatus = "UPDATE botdb.user SET status = '" + status + "'" +\
                   " WHERE tg_Name = '@" + user + "';"
        print(setstatus)
        with connection.cursor() as cursor:
            cursor.execute(setstatus)
            connection.commit()

def add_survey(user, survey_num, answer): # Добавить запись в опрос
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        add_survey_to_sql = "INSERT INTO botdb.survey_" + survey_num + " (tg_Name, question_1) " \
                             "VALUES ('@" + user + "','" + answer + "');"
        print(add_survey_to_sql)
        with connection.cursor() as cursor:
            cursor.execute(add_survey_to_sql)
            connection.commit()

def set_survey(user, survey_num, question_num, answer): # Дополнить запись в опросе
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        set_answer = "UPDATE botdb.survey_" + survey_num + " SET question_" + question_num + "='" + \
            answer + "' where tg_Name = '@" + user + "';"
        print(set_answer)
        with connection.cursor() as cursor:
            cursor.execute(set_answer)
            connection.commit()

def get_subdvsn(user):
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        select_subdvsn = "SELECT * FROM botdb.subdivision WHERE idSubdivision = (SELECT"\
        " key_id_subd FROM botdb.user WHERE tg_Name = '@" + user + "');"
        print(select_subdvsn)
        with connection.cursor() as cursor:
            cursor.execute(select_subdvsn)
            words = list(cursor.fetchall()[0])
            print(words)
            text_message = 'Вы работаете в: '+words[1] + ' \nпо адресу: '+\
                           words[2]
            return text_message

def get_hr():
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        select_hr = "SELECT chat_id FROM botdb.hr WHERE tg_Name_HR is not null;"
        print(select_hr)
        with connection.cursor() as cursor:
            cursor.execute(select_hr)
            hr=cursor.fetchall()[0][0]
            return hr

def add_task(message):
    split_msg = re.split(",|q3x9Z2K79D2|, ", message.text)
    task = split_msg[-1]
    user = split_msg[2]
    print(task)
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        set_task = "UPDATE botdb.user SET task = '" + task +" 'WHERE tg_Name='" + user + "';"
        print(set_task)
        with connection.cursor() as cursor:
            cursor.execute(set_task)
            connection.commit()

def get_task(user):
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        select_task = "SELECT task FROM botdb.user WHERE tg_Name = '@" + user + "';"
        print(select_task)
        with connection.cursor() as cursor:
            cursor.execute(select_task)
            task=cursor.fetchall()[0][0]
            return 'Твои задачи на испытательный срок: ' + str(task or 'пока нет с:')

def add_request(user, chat_id):
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        req = "INSERT INTO botdb.requests(tg_Name, chat_id) VALUES ('@" + user + "', '" + str(chat_id) + "');"
        print(req)
        with connection.cursor() as cursor:
            cursor.execute(req)
            connection.commit()

def get_request(user):
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        req = "SELECT chat_id FROM botdb.requests WHERE tg_Name = '" + user + "';"
        print(req)
        with connection.cursor() as cursor:
            cursor.execute(req)
            id=cursor.fetchall()[0][0]
            return id

def del_request(user):
    with connect(
            host="localhost",
            user="root",
            password="54321",
    ) as connection:
        req = "DELETE FROM botdb.requests WHERE tg_Name = '"+user+"';"
        print(req)
        with connection.cursor() as cursor:
            cursor.execute(req)
            connection.commit()
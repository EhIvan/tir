import telebot
import sqlite3
from sqlite3 import Error
from datetime import datetime, date, time

eholandbot = telebot.TeleBot('5390922879:AAGQPYKFnmp1GzxDUUoHV22Vk9GnbuohoGw')
from telebot import types

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

user_id = 0
path = "C:\\Users\\79175\\Documents\\GitHub\\tir\\src\\tir_db\\tir_db.db"  # Адрес БД


# Функции для регистрации пользователя.

def get_name(message):  # получаем имя вносим в БД имя и telegram_id, задаем вопрос про Фамилиюё
    name = message.text
    print("name=", name)
    print(message.from_user.id)
    telegram_id = message.from_user.id
    connection = create_connection(path)
    registration_script = f"""
            INSERT INTO User (telegram_id, name)
            VALUES ("{telegram_id}", "{name}")
            """
    result = execute_insert_query(connection, registration_script)
    print(result)
    surname = eholandbot.send_message(chat_id=message.chat.id, text='Какая у тебя фамилия?')
    eholandbot.register_next_step_handler(surname, get_surname)


def get_surname(message):
    surname = message.text
    telegram_id = message.from_user.id
    connection = create_connection(path)
    registration_script = f"""
            update user
            SET
            surname="{surname}"
            where telegram_id="{telegram_id}"
            """
    print(registration_script)
    result = execute_insert_query(connection, registration_script)
    print(result)
    mobile = eholandbot.send_message(chat_id=message.chat.id, text='Твой мобильный номер?')
    eholandbot.register_next_step_handler(mobile, get_mobile)


def get_mobile(message):
    mobile = message.text
    # print(message.from_user.id)
    telegram_id = message.from_user.id
    connection = create_connection(path)
    registration_script = f"""
                update user
                SET
                mobile="{mobile}"
                where telegram_id="{telegram_id}"
                """
    result = execute_insert_query(connection, registration_script)
    print(result)
    car_info = eholandbot.send_message(chat_id=message.chat.id, text='Введите марку и гос. номер ваших машин')
    eholandbot.register_next_step_handler(car_info, get_car_info)


def get_car_info(message):
    car_info = message.text
    print(message.from_user.id)
    telegram_id = message.from_user.id
    connection = create_connection(path)
    registration_script = f"""
                update user
                SET
                    car_info="{car_info}"
                where telegram_id="{telegram_id}"
                """
    result = execute_insert_query(connection, registration_script)
    print(result)
    email = eholandbot.send_message(chat_id=message.chat.id, text='информация о почте?')
    eholandbot.register_next_step_handler(email, get_email)


def get_email(message):
    email = message.text
    print(message.from_user.id)
    telegram_id = message.from_user.id
    connection = create_connection(path)
    registration_script = f"""
                 update user
                 SET
                     email="{email}"
                 where telegram_id="{telegram_id}"
                 """
    result = execute_insert_query(connection, registration_script)
    print(result)
    eholandbot.send_message(chat_id=message.chat.id,
                            text='Подтвердить следующие данные для регистрации? \n''\n Для продолжения нажмите ДА',
                            reply_markup=keyboard_yes_no())


# Функции для определения ранга пользователя

def check_rank(user_id):  # Тянет из БД ранг стрелка: админ, тренер, стрелок
    check_rank = f"""
    select rank_name from
    rank
    inner join user using (rank_id)
    where telegram_id='{user_id}'
    """
    return check_rank


# Функция соединения с БД

def create_connection(path):  # Подключение к БД
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# Функция SELECT из БД

def execute_read_query(connection, query):  # По идее, универсальная функция под SELECT
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_insert_query(connection, query):  # По идее, универсальная функция под update, insert
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(query)

        # result = cursor.
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# Клавиатура да/нет для регистрации

def keyboard_yes_no():
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да, зарегистрировать', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='Нет, вернуться назад', callback_data='no')
    keyboard.add(key_yes, key_no)
    return keyboard


# Основная клавиатура

def keyboard_main(message):  # Первая клавиатура
    user_id = message.from_user.id
    connection = create_connection(path)
    script = check_rank(user_id)
    result = execute_read_query(connection, script)
    print(result)
    print(script)
    print(user_id)
    keyboard = types.InlineKeyboardMarkup()
    key_join_event = types.InlineKeyboardButton(text='Записаться', callback_data='join_event')
    key_cancel_event = types.InlineKeyboardButton(text='Отмена записи', callback_data='cancel_event')
    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    key_stat = types.InlineKeyboardButton(text='Показать статистику', callback_data='show_stat')
    key_new_event = types.InlineKeyboardButton(text='Создать новую тренировку', callback_data='create_new_event')
    key_registration = types.InlineKeyboardButton(text='Пройти регистрацию', callback_data='registration')
    print(result[0])

    if result == [('admin',)]:
        keyboard.add(key_join_event)
        keyboard.add(key_cancel_event, key_stat, key_new_event, key_registration)
        keyboard.add(key_back)
    elif result == [('trener',)]:
        keyboard.add(key_join_event)
        keyboard.add(key_cancel_event, key_stat, key_new_event)
        keyboard.add(key_back)
    elif result == [('shooter',)]:
        keyboard.add(key_join_event, key_cancel_event, key_stat)
        keyboard.add(key_back)
    elif result == [('new_bro',)]:
        eholandbot.send_message(message.chat.id, "Проверка пользователя, обратитесь к вашему тренеру")
        return None
    else:
        keyboard.add(key_registration)
        keyboard.add(key_back)
    eholandbot.send_message(message.from_user.id, text='sad', reply_markup=keyboard)


# Набросок клавиатуры для записи на тренировку

def keyboard_data():  # Набросок клавиатуры для записи на тренировку
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='2022.05.01', callback_data='trening_day'))
    keyboard.add(types.InlineKeyboardButton(text='2022.06.10', callback_data='Data_idn'))
    return keyboard







# Команды для бота


@eholandbot.message_handler(commands=['help'])
def send_welcome(message):
    eholandbot.reply_to(message, "Howdy, how are you doing?")

# Код для вывода всех мест и создания эвента
@eholandbot.message_handler(commands=['test'])
def keyboard_data_pleace(message):  # Набросок клавиатуры для записи на тренировку
    connection = create_connection(path)
    telegram_id = message.from_user.id
    script = """select * from pleace"""
    result = execute_read_query(connection, script)
    n = len(result)
    keyboard = types.InlineKeyboardMarkup()
    for i in range(0, n):
        keyboard.add(types.InlineKeyboardButton(text=f'{result[i][1]}', callback_data=f'{result[i][0]}'))
        print(result[i][1])
    registration_script = f"""
            INSERT INTO events (event_creator_id, date)
            VALUES ((select user_id from user where telegram_id={telegram_id}), "{result}")
            """
    print(registration_script)
    create_event = execute_insert_query(connection, registration_script)
    print(create_event)
    eholandbot.send_message(message.from_user.id, text='Выберите место', reply_markup=keyboard)

@eholandbot.message_handler(commands=['start'])  # Проверяем на команду /start, если она, идем дальше
def start(message):
    #user_id = message.from_user.id
    #connection = create_connection(path)
    #script = check_rank(user_id)
    #result = execute_read_query(connection, script)
    #print(result)
    #print(script)
    #print(user_id)
    eholandbot.send_message(message.from_user.id, 'Привет!, ')
    keyboard_main(message)


# Календарь
@eholandbot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    current_date = date.today()
    if not result and key:
        eholandbot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        eholandbot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
        print(result)




@eholandbot.callback_query_handler(func=lambda callback_data: True)  # Может быть только один
def ping_back(callback_data):
    if callback_data.data == 'trening_day':
        eholandbot.answer_callback_query(callback_data.id, 'Сейчас запишемся',
                                         show_alert=True)  # всплывающее уведомление о выбранном ответе, show_alert=True добавляет подтверждение пользователя
        eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
                                     text="Сейчас будем записываться на тренировку", reply_markup=None)
        eholandbot.send_message(callback_data.from_user.id, 'Выберите дату', reply_markup=keyboard_data())

    elif callback_data.data == 'cancel_trening_day':
        eholandbot.answer_callback_query(callback_data.id, 'Сейчас отменим')
        eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
                                     text="Сейчас будем отменять тренировку", reply_markup=None)

    elif callback_data.data == 'registration':  # Скрипт для регистрации пользователя
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        # eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id, reply_markup=None)
        name_ = eholandbot.send_message(chat_id=callback_data.message.chat.id, text='Как тебя зовут?')
        print(callback_data.from_user.id)
        eholandbot.register_next_step_handler(name_, get_name)  # следующий шаг – функция get_name
    elif callback_data.data == 'yes':
        eholandbot.answer_callback_query(callback_data.id, 'Регистрируемся...')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        telegram_id = callback_data.from_user.id
        print(telegram_id)
        connection = create_connection(path)
        registration_script = f"""
        UPDATE User 
        SET 
        rank_id = 4 
        WHERE telegram_id="{telegram_id}"
        """
        print(registration_script)
        result = execute_insert_query(connection, registration_script)
        print(result)
        eholandbot.send_message(callback_data.from_user.id, 'Ожидайте подтверждения от вашего тренера')
    elif callback_data.data == 'create_new_event':
        eholandbot.answer_callback_query(callback_data.id, 'Создаем...')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        calendar, step = DetailedTelegramCalendar().build()
        eholandbot.send_message(callback_data.message.chat.id, f"Select {LSTEP[step]}",
                         reply_markup=calendar)




# @eholandbot.message_handler(func=lambda m: True)
# def echo_all(message):
#    eholandbot.reply_to(message, message.text)


eholandbot.infinity_polling(2)

# запрос на моб номер

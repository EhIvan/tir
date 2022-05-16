import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, date, time
eholandbot = telebot.TeleBot('5390922879:AAGQPYKFnmp1GzxDUUoHV22Vk9GnbuohoGw')
import SQLite_function
#import main_function
import keyboard_function

@eholandbot.message_handler(commands=['help'])
def send_welcome(message):
    eholandbot.send_message(67585554, text='Как дела? если читаешь, пришли мне скрин))')


@eholandbot.message_handler(commands=['start'])  # Проверяем на команду /start, если она, идем дальше
def first_step(message):
#    telegram_id = message.from_user.id
    rank = SQLite_function.get_rank(message.from_user.id)
    print(rank)
    if len(rank) == 0:
        name = eholandbot.send_message(chat_id=message.chat.id, text='Для продолжения необходимо зарегестрироваться.\nКак тебя зовут?')
        eholandbot.register_next_step_handler(name, get_name)  # следующий шаг – функция get_name
    elif len(rank) == 1 and rank[0][1] == 'new_bro':
        eholandbot.send_message(message.from_user.id, text='Доступ ограничен, обратитесь к вашему тренеру.')
    elif len(rank) == 1:
        keyboard_function.keyboard_main(rank)
        eholandbot.send_message(message.from_user.id, text='Вам доступно:', reply_markup=keyboard_function.keyboard_main(rank))

"""# """
def get_name(message):  # получаем имя вносим в БД имя и telegram_id, задаем вопрос про Фамилиюё
    print(message.text)
    print(message.from_user.id)
    SQLite_function.create_user(message)
    data_user = ['telegram_id', 'name', 'surname', 'mobile', 'car_info', 'club_id', 'email']
    data_user[0] = message.from_user.id
    data_user[1] = message.text
    print(data_user)
    surname = eholandbot.send_message(chat_id=message.chat.id, text='Какая у тебя фамилия?')
    eholandbot.register_next_step_handler(surname, get_surname, data_user)


def get_surname(message, data_user):
    print(message.text)
    print(data_user)
    data_user[2] = message.text
    print(data_user)
    SQLite_function.update_user(message.from_user.id, surname=message.text, phone=None, car_info=None, email=None)
    phone = eholandbot.send_message(chat_id=message.chat.id, text="А теперь ваш номер..", reply_markup=keyboard_function.phone_keyboard())
    eholandbot.register_next_step_handler(phone, get_phone, data_user)


def get_phone(message, data_user):
    print('phone=', message.contact.phone_number)
    print(data_user)
    data_user[3] = message.contact.phone_number
    print(data_user)
    SQLite_function.update_user(message.from_user.id, surname=None, phone=message.contact.phone_number, car_info=message.text, email=None)
    car_info = eholandbot.send_message(chat_id=message.chat.id, text="Для вашего комфорта предоставте марку и гос. номер ВСЕХ ваших машин!", reply_markup=telebot.types.ReplyKeyboardRemove())
    eholandbot.register_next_step_handler(car_info, get_car_info, data_user)


def get_car_info(message, data_user):
    print('car_info=', message.text)
    print(data_user)
    data_user[4] = message.text
    print(data_user)
    SQLite_function.update_user(message.from_user.id, surname=None, phone=None, car_info=message.text,
                                email=None)
    eholandbot.send_message(chat_id=message.chat.id, text="Выберите ваш клуб",
                            reply_markup=keyboard_function.club_keyborad(SQLite_function.get_club()))

# def get_club_info(message):
#@eholandbot.message_handler(commands=['test'])
def get_club_info(message):
    club_list = SQLite_function.get_club()
    print(club_list)
    print(club_list[0])
    print(club_list[1])
    eholandbot.send_message(message.from_user.id, text='Выберите клуб',
                            reply_markup=keyboard_function.club_keyborad(club_list))

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
        if result < current_date:
            eholandbot.edit_message_text(f"Выбранная дата не может быть раньше чем  {current_date}!",
                                         c.message.chat.id,
                                         c.message.message_id)
            calendar, step = DetailedTelegramCalendar().build()
            eholandbot.send_message(c.message.chat.id, f"Select {LSTEP[step]}",
                                    reply_markup=calendar)
        else:
            eholandbot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
            date_event = result
            print(date_event)
            create_event_place_keyboard(c, date_event)


def create_event_place_keyboard(message, date_event):  # Набросок клавиатуры для записи на тренировку
    event_id = SQLite_function.create_event(message.from_user.id, date_event)
    place_list = SQLite_function.place_list()
    print(place_list)
    keyboard_function.place_keyboard(event_id, place_list)

"""#
#    connection = create_connection(path)
#    telegram_id = message.from_user.id
    #    #    registration_script = f"
    #                INSERT INTO events (event_creator_id, date)
    #                VALUES ((select user_id from user where telegram_id={telegram_id}), "{date_event}");
                "
    print(registration_script)
    create_event = execute_insert_query(connection, registration_script)
    print(create_event)
#    script = "select * from pleace"
    result = execute_read_query(connection, script)
    n = len(result)
    keyboard = types.InlineKeyboardMarkup()
    for i in range(0, n):
        keyboard.add(types.InlineKeyboardButton(text=f'{result[i][1]}', callback_data=f'pleace_{result[i][0]}'))
        print(result[i][1])
"""

@eholandbot.callback_query_handler(func=lambda callback_data: True)  # Может быть только один
def work_with_keyboard(callback_data):
#    if callback_data.data[0:4] == 'club_': # не работает
#       print("да")
#            eholandbot.answer_callback_query(callback_data.id, 'Сейчас отменим')
#       eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
#                                     text="Подтверждаете регистрацию?", reply_markup=None)
#        eholandbot.send_message(callback_data.from_user.id, 'Выберите дату')
    if callback_data.data.startswith('club_') == True:
#        eholandbot.answer_callback_query(callback_data.id, '')
        SQLite_function.create_user_rank(callback_data, callback_data.from_user.id)
        eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
                                     text="Регистрация пройдена, ожидайте подтверждение от вашего тренера", reply_markup=None)
        trener_notificatipon(callback_data.data[5:])
    elif callback_data.data.startswith('approve_') == True:
        print(callback_data.data)
        SQLite_function.update_rank(callback_data.data.split('_')[1], callback_data.data.split('_')[2], "strelok")
        eholandbot.send_message(callback_data.data.split('_')[3], text='Вы приняты!')
    elif callback_data.data.startswith('reject_') == True:
        print(callback_data.data)
#        SQLite_function. Ничего удалять нельзя, т.к. если человек состоит в двух клубах, то все сломается, нужна проверка.
        eholandbot.send_message(callback_data.data.split('_')[3], text='Вы не приняты! Поговорите с вашим тренером')
    elif callback_data.data.startswith('key_new_event'):
        eholandbot.answer_callback_query(callback_data.id, 'Процедура создание новой тренировки')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        calendar, step = DetailedTelegramCalendar().build()
        eholandbot.send_message(callback_data.from_user.id, f"Select {LSTEP[step]}", reply_markup=calendar)

    else: eholandbot.send_message(callback_data.from_user.id, 'Я этому еще не обучен...')

""""
key_list_event
key_list_user_event
key_get_new_bro_list
key_new_event
key_back
"""




def trener_notificatipon(club_id):
    new_bro_list = SQLite_function.get_new_bro_list(club_id)
    trener_list = SQLite_function.get_trener_list(club_id)
    print(new_bro_list)
    print(trener_list)

    for new_bro in new_bro_list:
        for trener in trener_list:
            eholandbot.send_message(trener[0], text=f'Поступила заявка от {new_bro[1]} {new_bro[2]} \n {new_bro[3]}',
                                reply_markup=keyboard_function.new_bro_approve(new_bro[0], club_id, new_bro[4]))



eholandbot.infinity_polling(2)
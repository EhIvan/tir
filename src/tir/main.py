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
        name = eholandbot.send_message(chat_id=message.chat.id, text='Привет! Это бот клуба A-Shooting. Пожалуйста, зарегистрируйтесь для продолжения. \n Укажите Ваше имя')
        eholandbot.register_next_step_handler(name, get_name)  # следующий шаг – функция get_name
    elif len(rank) == 1 and rank[0][1] == 'new_bro':
        eholandbot.send_message(message.from_user.id, text='Доступ ограничен, обратитесь к вашему тренеру.')
    elif len(rank) == 1:
        keyboard_function.keyboard_main(rank)
        eholandbot.send_message(message.from_user.id, text='Вам доступно:', reply_markup=keyboard_function.keyboard_main(rank))
#    elif len(rank) > 1: Даллее шаг с выбором конкретного клуба, и передача в дальнейшие шаги, конкретной строки: rank[i]

"""# """
def get_name(message):  # получаем имя вносим в БД имя и telegram_id, задаем вопрос про Фамилиюё
    print(message.text)
    print(message.from_user.id)
    SQLite_function.create_user(message)
    data_user = ['telegram_id', 'name', 'surname', 'mobile', 'car_info', 'club_id', 'email']
    data_user[0] = message.from_user.id
    data_user[1] = message.text
    print(data_user)
    surname = eholandbot.send_message(chat_id=message.chat.id, text='Укажите Вашу фамилию')
    eholandbot.register_next_step_handler(surname, get_surname, data_user)


def get_surname(message, data_user):
    print(message.text)
    print(data_user)
    data_user[2] = message.text
    print(data_user)
    SQLite_function.update_user(message.from_user.id, surname=message.text, phone=None, car_info=None, email=None)
    phone = eholandbot.send_message(chat_id=message.chat.id, text="""Укажите Ваш номер телефона.\nДля этого нажмите на кнопку "Отправить номер телефона" внизу экрана⬇""", reply_markup=keyboard_function.phone_keyboard())
    eholandbot.register_next_step_handler(phone, get_phone, data_user)


def get_phone(message, data_user):
    print('phone=', message.contact.phone_number)
    print(data_user)
    data_user[3] = message.contact.phone_number
    print(data_user)
    SQLite_function.update_user(message.from_user.id, surname=None, phone=message.contact.phone_number, car_info=message.text, email=None)
    car_info = eholandbot.send_message(chat_id=message.chat.id, text="Добавьте марку и гос номер Вашей машины (мотоцикла) в формате «Мерседес, х111х111». Если вы планируете приезжать на разных автомобилях, то добавьте их все. Если у Вас нет машины, напишите Нет",
                                       reply_markup=telebot.types.ReplyKeyboardRemove())
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
            update_event_place(c, date_event)


def update_event_place(c, date_event):
    telegram_id = c.from_user.id
    event_id = SQLite_function.get_event_id(telegram_id)[0][0]
    print("update_event_place перед запуском update_event c датой", event_id)
    SQLite_function.update_event(event_id, date=date_event, time=None, trener_id=None, category_id=None, comment=None)
    time_event = eholandbot.send_message(chat_id=c.message.chat.id, text="Укажите время начала тренировки")
    eholandbot.register_next_step_handler(time_event, update_time, event_id)


def update_time(time_event, event_id):
    print("update_time", event_id)
    SQLite_function.update_event(event_id, date=None, time=time_event.text, trener_id=None, category_id=None, comment=None)
    eholandbot.send_message(chat_id=time_event.chat.id, text="Выберите тренера на тренировку:",
                                        reply_markup=keyboard_function.club_trener(event_id))

# Разобраться с переменной event_id.
def update_trener(callback_data):
    user_id = callback_data.data.split('/')[1]
    event_id = callback_data.data.split('/')[2]
    print("update_trener event_id", event_id)
    print("update_trener user_id", user_id)
    SQLite_function.update_event(event_id, date=None, time=None, trener_id=user_id, category_id=None,
                                 comment=None)
    eholandbot.send_message(chat_id=callback_data.message.chat.id, text="Выберите дисциплину тренировки:",
                                        reply_markup=keyboard_function.event_category(event_id))


def update_category(callback_data):
    category_id = callback_data.data.split('/')[1]
    event_id = callback_data.data.split('/')[2]
    print("update_category event_id", event_id)
    print("update_category user_id", category_id)
    SQLite_function.update_event(event_id, date=None, time=None, trener_id=None, category_id=category_id,
                                 comment=None)
    comment = eholandbot.send_message(chat_id=callback_data.message.chat.id, text="Внесите комментарии к тренировке")
    eholandbot.register_next_step_handler(comment, update_comment, event_id)


def update_comment(message, event_id):
    SQLite_function.update_event(event_id, date=None, time=None, trener_id=None, category_id=None, comment=message.text)
    eholandbot.send_message(message.from_user.id, "Тренировка создана")


def create_event_place_keyboard(message):  # Набросок клавиатуры для записи на тренировку
#    event_id = SQLite_function.create_event(message.from_user.id, date_event)
    print("Сюда пришло", message.data)
    club_id =message.data.split('/')[1]
    print(club_id)
    place_list = SQLite_function.place_list()
    print(place_list)
    eholandbot.send_message(message.from_user.id, "Выберите место проведения тренировки:",
                            reply_markup=keyboard_function.place_keyboard(club_id, place_list))

@eholandbot.callback_query_handler(func=lambda callback_data: True)  # Может быть только один
def work_with_keyboard(callback_data):
    if callback_data.data.startswith('club_') == True:
        SQLite_function.create_user_rank(callback_data, callback_data.from_user.id)
        eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
                                     text="Регистрация пройдена, ожидайте подтверждение от вашего тренера", reply_markup=None)
        trener_notificatipon(callback_data.data[5:])
    elif callback_data.data.startswith('approve_') == True:
        print(callback_data.data)
        SQLite_function.update_rank(callback_data.data.split('_')[1], callback_data.data.split('_')[2], "strelok")
        eholandbot.send_message(callback_data.data.split('_')[3], text='Вы приняты!')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
    elif callback_data.data.startswith('reject_') == True:
        print(callback_data.data)
#        SQLite_function. Ничего удалять нельзя, т.к. если человек состоит в двух клубах, то все сломается, нужна проверка.
        eholandbot.send_message(callback_data.data.split('_')[3], text='Вы не приняты! Поговорите с вашим тренером')
    elif callback_data.data.startswith('key_new_event'):
        eholandbot.answer_callback_query(callback_data.id, 'Процедура создание новой тренировки')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        create_event_place_keyboard(callback_data)
#        calendar, step = DetailedTelegramCalendar().build()
#        eholandbot.send_message(callback_data.from_user.id, f"Select {LSTEP[step]}", reply_markup=calendar)
    elif callback_data.data.startswith('create_event_in_place'):
        eholandbot.answer_callback_query(callback_data.id, 'Место выбрано')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        club_id = callback_data.data.split("/")[2]
        place_id = callback_data.data.split("/")[1]
        telegram_id = callback_data.from_user.id
        SQLite_function.create_event(telegram_id, place_id, club_id)
        calendar, step = DetailedTelegramCalendar().build()
        eholandbot.send_message(callback_data.from_user.id, f"Select {LSTEP[step]}", reply_markup=calendar)
    elif callback_data.data.startswith('event_trener'):
        eholandbot.answer_callback_query(callback_data.id, 'Тренер выбран')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        update_trener(callback_data)
    elif callback_data.data.startswith('event_category'):
        eholandbot.answer_callback_query(callback_data.id, 'Категория выбрана')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        print(callback_data.data)
        update_category(callback_data)
    elif callback_data.data.startswith('key_list_event'):
        eholandbot.answer_callback_query(callback_data.id, 'Загружем список доступных тренировок')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        show_event_list(callback_data)
    elif callback_data.data.startswith("event_keyboard"):
        print(callback_data.data)
        eholandbot.answer_callback_query(callback_data.id, 'Меню тренировки')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        event_menu(callback_data)
    elif callback_data.data.startswith("key_registration"):
        eholandbot.answer_callback_query(callback_data.id, 'Участие в тренировке подтверждено', show_alert=True)
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        SQLite_function.registration(callback_data.from_user.id, callback_data.data.split("/")[1],
                                            callback_data.data.split("/")[2])
    elif callback_data.data.startswith("key_cancel_registration"):
        eholandbot.answer_callback_query(callback_data.id, 'Участие в тренировке отменено', show_alert=True)
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        SQLite_function.cancel_registration(callback_data.from_user.id, callback_data.data.split("/")[1],
                                            callback_data.data.split("/")[2])
    elif callback_data.data.startswith("key_delete_event"):
        eholandbot.answer_callback_query(callback_data.id, 'Тренировка отменена', show_alert=True)
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        user_list = SQLite_function.show_user_event(callback_data.data.split("/")[2])
        event_info = SQLite_function.get_event_info(callback_data.data.split("/")[2])
        # date, time, place_name, name, surname, category_name, comment, event_id, club_id
        for item in user_list:
            eholandbot.send_message(chat_id=item[3], text=f'Тренировка {event_info[0][0]} в категории {event_info[0][5]} на территории {event_info[0][2]} отменена, будте внимательны!')
        SQLite_function.delete_event(callback_data.from_user.id, callback_data.data.split("/")[1],
                                            callback_data.data.split("/")[2])
    elif callback_data.data.startswith("key_show_user_event"):
        eholandbot.answer_callback_query(callback_data.id, 'Грузим списки...')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        user_event = SQLite_function.show_user_event(callback_data.data.split("/")[1])
        print(user_event)
        text = "Список участников"
        for item in user_event:
            text += f"""\n{item[0]} {item[1]} {item[2]}"""
        print(text)
        eholandbot.send_message(callback_data.from_user.id, text=f'{text}')
    elif callback_data.data.startswith("key_get_new_bro_list"):
        eholandbot.answer_callback_query(callback_data.id, 'Грузим списки...')
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)
        get_new_bro_list(callback_data)
    elif callback_data.data.startswith("key_list_user_event"):
        eholandbot.answer_callback_query(callback_data.id, 'Грузим списки..., но фича в процессе', show_alert=True)
        eholandbot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)


    else: eholandbot.send_message(callback_data.from_user.id, 'Я этому еще не обучен...')

""""
key_list_event  - готово
key_list_user_event
key_get_new_bro_list - готово
key_new_event - готово
key_back

key_registration key_registration/{club_id}/{event_id}  - готово
key_cancel_registration  - готово
key_show_user_event   - готово
key_delete_event  - готово

"""
def event_menu(callback_data):
    club_id = callback_data.data.split('/')[2]
    event_id = callback_data.data.split('/')[1]
    telegram_id = callback_data.from_user.id
    rank = SQLite_function.get_rank_for_event(telegram_id, club_id)
    print(rank[0][1])
    reg_info = SQLite_function.get_reg_info(telegram_id, event_id)
    print(reg_info)
    eholandbot.send_message(callback_data.from_user.id, f"Вам доступны следующие действия для этого мероприятия:",
                            reply_markup=keyboard_function.one_event_menu(rank, reg_info, event_id))
# Для данного шага нужен статус пользователя из таблицы User_rank
# и есть ли user_id пользователя в таблице user_event с требуемым event_id: если есть до клавиша отмены регистрации, если нет, то клавиша зарегестрироваться
#event_keyboard/49/1


def show_event_list(callback_data):
    telegram_id = callback_data.from_user.id
    club_id = callback_data.data.split("/")[1]
    event_list = SQLite_function.get_event_list(club_id)
    print("event_list", event_list)
    print("telegram_id", telegram_id)
    print("club_id", club_id)
    for item in event_list:
        eholandbot.send_message(callback_data.from_user.id, f"Тренировка в {item[2]} {item[0]} {item[1]} "
                                                            f"\n Тренер: {item[4]} в дисциплине {item[5]}"
                                                            f"\n Комментарий: {item[6]}",
                                reply_markup=keyboard_function.event_keyboard(item))

    # SELECT date, time, place_name, name, surname, category_name, comment, event_id, club_id

def trener_notificatipon(club_id):
    new_bro_list = SQLite_function.get_new_bro_list(club_id)
    trener_list = SQLite_function.get_trener_list(club_id)
    print(new_bro_list)
    print(trener_list)

    for new_bro in new_bro_list:
        for trener in trener_list:
            eholandbot.send_message(trener[0], text=f'Поступила заявка от {new_bro[1]} {new_bro[2]} \n {new_bro[3]}',
                                reply_markup=keyboard_function.new_bro_approve(new_bro[0], club_id, new_bro[4]))

def get_new_bro_list(callback_data):
    club_id = callback_data.data.split("/")[1]
    new_bro_list = SQLite_function.get_new_bro_list(club_id)
    print(new_bro_list)
    for new_bro in new_bro_list:
            eholandbot.send_message(callback_data.from_user.id, text=f'Поступила заявка от {new_bro[1]} {new_bro[2]} \n {new_bro[3]}',
                                reply_markup=keyboard_function.new_bro_approve(new_bro[0], club_id, new_bro[4]))


eholandbot.infinity_polling(25)
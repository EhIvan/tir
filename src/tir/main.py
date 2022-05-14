import telebot

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
@eholandbot.message_handler(commands=['test'])
def get_club_info(message):
    club_list = SQLite_function.get_club()
    print(club_list)
    print(club_list[0])
    print(club_list[1])
    eholandbot.send_message(message.from_user.id, text='Выберите клуб',
                            reply_markup=keyboard_function.club_keyborad(club_list))


@eholandbot.callback_query_handler(func=lambda callback_data: True)  # Может быть только один
def work_with_keyboard(callback_data, data_user):
    print(callback_data.data[0:5])
    print(callback_data.data[5:])
    if callback_data.data[0:4] == 'club_': # не работает
        print("да")
        eholandbot.answer_callback_query(callback_data.id, 'Сейчас отменим')
        eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
                                     text="Подтверждаете регистрацию?", reply_markup=None)
        eholandbot.send_message(callback_data.from_user.id, 'Выберите дату')
    elif callback_data.data.startswith('club_') == True:
        print("ofcorse")
        eholandbot.answer_callback_query(callback_data.id, '')

        eholandbot.edit_message_text(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id,
                                     text="Подтверждаете регистрацию?", reply_markup=None)


eholandbot.infinity_polling(2)
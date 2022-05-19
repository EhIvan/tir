from telebot import types

import SQLite_function


def phone_keyboard():
    phone_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone_keyboard.add(types.KeyboardButton(text="Нажмите на кнопку", request_contact=True))
    return phone_keyboard


def phone_keyboard2():
    phone_keyboard2 = types.InlineKeyboardMarkup()
    phone_keyboard2.add(types.InlineKeyboardButton(text='Нажмите на кнопку', callback_data='trening_day', request_contact=True))
    return phone_keyboard2

def club_keyborad(club_list):
    print(len(club_list))
    club_keyboard = types.InlineKeyboardMarkup()
#    for i in range(0, n):
#        club_keyboard.add(types.InlineKeyboardButton(text=f'{result[i][1]}', callback_data=f'club_{result[i][0]}'))
#        print(result[i][1])
    for item in club_list:
        club_keyboard.add(types.InlineKeyboardButton(text=f'{item[1]}', callback_data=f'club_{item[0]}'))
# print(club_list[1])

    return club_keyboard


def event_keyboard(event_list):
    # SELECT date, time, place_name, name, surname, category_name, comment, event_id, club_id
    print(event_list)
    event_keyboard = types.InlineKeyboardMarkup()
    event_keyboard.add(types.InlineKeyboardButton(text="Записаться", callback_data=f'event_keyboard/{event_list[7]}/{event_list[8]}'))
    return event_keyboard

def club_trener(event_id):
    print("keyclub_trener", event_id)
    trener_list_for_event = SQLite_function.get_trener_list_for_event(event_id)
    print(trener_list_for_event)
    club_trener = types.InlineKeyboardMarkup()
    for item in trener_list_for_event:
        club_trener.add(types.InlineKeyboardButton(text=f'{item[0]} {item[1]}',
                                                   callback_data=f'event_trener/{item[2]}/{event_id}'))
    return club_trener


def event_category(event_id):
    category_list = SQLite_function.category_list()
    event_category = types.InlineKeyboardMarkup()
    for item in category_list:
        event_category.add(types.InlineKeyboardButton(text=f'{item[1]}',
                                                   callback_data=f'event_category/{item[0]}/{event_id}'))
    return event_category


def place_keyboard(club_id, place_list):

    place_keyboard = types.InlineKeyboardMarkup()
    for item in place_list:
        place_keyboard.add(types.InlineKeyboardButton(text=f'{item[1]}', callback_data=f'create_event_in_place/{item[0]}/{club_id}'))
    return place_keyboard

def new_bro_approve(user_id, club_id, telegram_id):
    new_bro_keyboard = types.InlineKeyboardMarkup()
    new_bro_keyboard.add(types.InlineKeyboardButton(text='Принять', callback_data=f'approve_{user_id}_{club_id}_{telegram_id}'),
                           types.InlineKeyboardButton(text='Отказать', callback_data=f'reject_{user_id}_{club_id}_{telegram_id}'))
    return new_bro_keyboard

def keyboard_main(rank):
    keyboard = types.InlineKeyboardMarkup()
    key_list_event = types.InlineKeyboardButton(text='Доступные мероприятия', callback_data=f'key_list_event/{rank[0][2]}') # в rank[0][2] передается club_id
    key_cancel_event = types.InlineKeyboardButton(text='Отмена записи', callback_data=f'key_cancel_event/{rank[0][2]}')
    key_back = types.InlineKeyboardButton(text='Назад', callback_data=f'back')
    key_new_event = types.InlineKeyboardButton(text='Добавить мероприятие', callback_data=f'key_new_event/{rank[0][2]}')
    key_list_user_event = types.InlineKeyboardButton(text='Получить список участников мероприятия',
                                                     callback_data=f'key_list_user_event/{rank[0][2]}')
    key_get_new_bro_list = types.InlineKeyboardButton(text='Список заявок на вступление',
                                                     callback_data=f'key_get_new_bro_list/{rank[0][2]}')
    print(rank[0][1])

    if rank[0][1] == 'admin':
        keyboard.add(key_list_event)
        keyboard.add(key_list_user_event, key_get_new_bro_list)
        keyboard.add(key_new_event)
        keyboard.add(key_back)
    elif rank[0][1] == 'trener':
        keyboard.add(key_list_event)
        keyboard.add(key_get_new_bro_list, key_new_event)
        keyboard.add(key_back)
    elif rank[0][1] == 'strelok':
        keyboard.add(key_list_event)
        keyboard.add(key_back)
        print('strelok_i am there')
    else:
        keyboard.add(key_back)
    return keyboard
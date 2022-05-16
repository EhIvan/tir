from telebot import types
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

def place_keyboard(event_id, place_list):



def new_bro_approve(user_id, club_id, telegram_id):
    new_bro_keyboard = types.InlineKeyboardMarkup()
    new_bro_keyboard.add(types.InlineKeyboardButton(text='Принять', callback_data=f'approve_{user_id}_{club_id}_{telegram_id}'),
                           types.InlineKeyboardButton(text='Отказать', callback_data=f'reject_{user_id}_{club_id}_{telegram_id}'))
    return new_bro_keyboard

def keyboard_main(rank):
    keyboard = types.InlineKeyboardMarkup()
    key_list_event = types.InlineKeyboardButton(text='Доступные мероприятия', callback_data='key_list_event')
    key_cancel_event = types.InlineKeyboardButton(text='Отмена записи', callback_data='key_cancel_event')
    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    key_new_event = types.InlineKeyboardButton(text='Добавить мероприятие', callback_data='key_new_event')
    key_list_user_event = types.InlineKeyboardButton(text='Получить список участников мероприятия',
                                                     callback_data='key_list_user_event')
    key_get_new_bro_list = types.InlineKeyboardButton(text='Список заявок на вступление',
                                                     callback_data='key_get_new_bro_list')
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
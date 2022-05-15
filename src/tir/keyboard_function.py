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



def new_bro_approve(user_id, club_id, telegram_id):
    new_bro_keyboard = types.InlineKeyboardMarkup()
    new_bro_keyboard.add(types.InlineKeyboardButton(text='Принять', callback_data=f'approve_{user_id}_{club_id}_{telegram_id}'),
                           types.InlineKeyboardButton(text='Отказать', callback_data=f'reject_{user_id}_{club_id}_{telegram_id}'))
    return new_bro_keyboard
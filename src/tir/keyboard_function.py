from telebot import types
def phone_keyboard():
    phone_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone_keyboard.add(types.KeyboardButton(text="Нажмите на кнопку", request_contact=True))
    return phone_keyboard


def phone_keyboard2():
    phone_keyboard2 = types.InlineKeyboardMarkup()
    phone_keyboard2.add(types.InlineKeyboardButton(text='Нажмите на кнопку', callback_data='trening_day', request_contact=True))
    return phone_keyboard2
import telebot
eholandbot = telebot.TeleBot('5390922879:AAGQPYKFnmp1GzxDUUoHV22Vk9GnbuohoGw')
from telebot import types



@eholandbot.message_handler(commands=['help'])
def send_welcome(message):
    eholandbot.reply_to(message, "Howdy, how are you doing?")


@eholandbot.message_handler(commands=['start'])
def start(message):
  user_id = message.from_user.id
  if user_id == 67585554:
    eholandbot.send_message(message.from_user.id, 'Петька, привет! что ты хочешь?')
  elif user_id == 271179022:

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2);
    key_yes = types.InlineKeyboardButton(text='Записаться', callback_data='trening_day');
    keyboard.add(key_yes);
    key_no = types.InlineKeyboardButton(text='Отмена записи', callback_data='cancel_trening_day');
    keyboard.add(key_no);
    eholandbot.send_message(message.from_user.id, '!!, привет!', reply_markup=keyboard)

  else:
      eholandbot.send_message(message.from_user.id, 'я тебя не знаю')
@eholandbot.message_handler(func=lambda m: True)
def echo_all(message):
    eholandbot.reply_to(message, message.text)

eholandbot.infinity_polling()


# вытащить ID отправителя, запрос на моб номер
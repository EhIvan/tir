import sqlite3
from sqlite3 import Error


DataBasePath = f"../TIRDB"  # Адрес БД

def create_connection():  # Подключение к БД
    connection = None
    try:
        connection = sqlite3.connect(DataBasePath)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def AddNewUser(name, telegramId):
    connection = reate_connection()
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(f"""INSERT INTO User (telegram_id, name) VALUES ("{telegramId}", '"{name}"')""")
        result = cursor.lastrowid
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def UpdateUser(telegramId, longname=None, car_info =None, email=None, phone=None):
    connection = reate_connection()
    cursor = connection.cursor()
    result = None
    #TODO: Сделать проверку пустых значений, чтобы не перетирать имеющиеся данные в БД
    try:
        with connection:
            cursor.execute(f"""UPDATE USER SET longname='{longname}', car_info = '{car_info}', email='{email}', phone = '{phone}' where telegram_id="{telegram_id}""")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def GetClubs():
    connection = reate_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute("""SELECT club_id, club_name, club_info FROM club""")
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def AddUserRole(telegram_id, clubname, rankname):
    connection = reate_connection()
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(f"""Insert INTO user_rank (user_id, rank_id) VALUES ((SELECT user_id FROM User WHERE telegram_id = {telegram_id}), (SELECT rank_id FROM RANK INNER JOIN CLUB ON rank.club_id = club.club_id where club_name = '{clubname}' and rank_name = "{rankname}"))""")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


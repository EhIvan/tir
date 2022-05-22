# Файл для работы с БД

import sqlite3
from sqlite3 import Error
from datetime import datetime, date, time
# Путь к БД
#DataBasePath = "C:\\Users\\79175\\Documents\\GitHub\\tir\\src\\tir_db\\tir_db.db"  # Адрес старой БД
#DataBasePath = "C:\\Users\\79175\\Documents\\GitHub\\tir\\src\\TIRDB.db"  # Адрес БД


DataBasePath = f"../TIRDB"  # Относительный адрес БД

# Функция соединения с БД
def create_connection(DataBasePath):  # Путь к БД указан сразу. Путь относительный
    connection = None
    try:
        connection = sqlite3.connect(DataBasePath)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def get_event_list(club_id):
    connection = create_connection(DataBasePath)
    script = f"""
SELECT date, time, place_name, name, surname, category_name, comment, event_id, club_id
from event
inner join place USING (place_id)
inner JOIN user on event.trener_id=user.user_id
inner JOIN category using (category_id)
WHERE club_id={club_id} and date>='{date.today()}'
"""
    print(date.today())
    print(script)
    cursor = connection.cursor()
    event_list = None
    try:
        cursor.execute(script)
        event_list = cursor.fetchall()
        return event_list
    except Error as e:
        print(f"The error '{e}' occurred")


def get_event_info(event_id):
    connection = create_connection(DataBasePath)
    script = f"""
SELECT date, time, place_name, name, surname, category_name, comment, event_id, club_id
from event
inner join place USING (place_id)
inner JOIN user on event.trener_id=user.user_id
inner JOIN category using (category_id)
WHERE event_id={event_id}
"""
    print(date.today())
    print(script)
    cursor = connection.cursor()
    event_info = None
    try:
        cursor.execute(script)
        event_info = cursor.fetchall()
        return event_info
    except Error as e:
        print(f"The error '{e}' occurred")


def create_event(telegram_id, place_id, club_id):
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    registration_script = f"""
                INSERT INTO event (event_creator_id, place_id, club_id)
                VALUES ((select user_id from user where telegram_id={telegram_id}),{place_id}, {club_id});
                """
    print(registration_script)
    try:
        with connection:
            cursor.execute(registration_script)
        print(cursor.lastrowid)
        event_id = cursor.lastrowid
        # result = cursor.
        return event_id

    except Error as e:
        print(f"The error '{e}' occurred")


def update_event(event_id, date=None, time=None, trener_id=None, category_id=None, comment=None):
    print("Внутри SQL Функции", event_id)
    text = """update event
              SET \n"""
    if date != None:
        text += f"""date='{date}'"""
    if time != None:
        text += f"""time='{time}'"""
    if trener_id != None:
        text += f"""trener_id='{trener_id}'"""
    if category_id != None:
        text += f"""category_id='{category_id}'"""
    if comment != None:
        text += f"""comment='{comment}'"""
    text += f"""\nWHERE event_id='{event_id}'"""
    print(text)
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(text)
        print(cursor.lastrowid)
        return result

    except Error as e:
        print(f"The error '{e}' occurred")


def get_event_id(telegram_id):
    connection = create_connection(DataBasePath)
    script = f"""
select max(event_id) from event
inner join user on event.event_creator_id=user.user_id
where telegram_id={telegram_id}
"""
    cursor = connection.cursor()
    event_id = None
    try:
        cursor.execute(script)
        event_id = cursor.fetchall()
        return event_id
    except Error as e:
        print(f"The error '{e}' occurred")



def place_list():
    connection = create_connection(DataBasePath)
    script = "select * from place"
    cursor = connection.cursor()
    place_list = None
    try:
        cursor.execute(script)
        place_list = cursor.fetchall()
        return place_list
    except Error as e:
        print(f"The error '{e}' occurred")


# Получаем все ранги пользователя в различных клубах
def get_rank(telegram_id):
    connection = create_connection(DataBasePath)
    script = f'''
    select rank_id, rank_name, club_id, club_name from
    rank
    inner join user_rank USING (rank_id)
    inner join user USING (user_id)
    inner JOIN club using (club_id)
    where telegram_id={telegram_id}
    '''
    cursor = connection.cursor()
    rank = None
    try:
        cursor.execute(script)
        rank = cursor.fetchall()
        return rank
    except Error as e:
        print(f"The error '{e}' occurred")


def get_rank_for_event(telegram_id, club_id):
    connection = create_connection(DataBasePath)
    script = f'''
    select rank_id, rank_name, club_id, club_name 
    from rank
    inner join user_rank USING (rank_id)
    inner join user USING (user_id)
    inner JOIN club using (club_id)
    where telegram_id={telegram_id} and club_id = {club_id}
    '''
    cursor = connection.cursor()
    rank = None
    try:
        cursor.execute(script)
        rank = cursor.fetchall()
        return rank
    except Error as e:
        print(f"The error '{e}' occurred")


def get_reg_info(telegram_id, event_id):
    connection = create_connection(DataBasePath)
    script = f'''
select * from user_event
inner join user using (user_id)
WHERE telegram_id ={telegram_id} and event_id= {event_id}
    '''
    cursor = connection.cursor()
    reg_info = None
    try:
        cursor.execute(script)
        reg_info = cursor.fetchall()
        return reg_info
    except Error as e:
        print(f"The error '{e}' occurred")



def show_user_event(event_id):
    connection = create_connection(DataBasePath)
    script = f'''
select name, surname, car_info,telegram_id
from user
inner JOIN user_event USING (user_id)
WHERE event_id={event_id}
     '''
    cursor = connection.cursor()
    user_event = None
    try:
        cursor.execute(script)
        user_event = cursor.fetchall()
        return user_event
    except Error as e:
        print(f"The error '{e}' occurred")



def cancel_registration(telegram_id, club_id, event_id):
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    cancel_script = f"""
DELETE FROM user_event
WHERE user_id=
(select user_id from user where telegram_id={telegram_id})
 and event_id={event_id}"""
    try:
        with connection:
            cursor.execute(cancel_script)
        print(cursor.lastrowid)
        # result = cursor.
        return result

    except Error as e:
        print(f"The error '{e}' occurred")


def registration(telegram_id, club_id, event_id):
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    cancel_script = f"""
            INSERT INTO user_event (user_id, event_id)
            VALUES ((select user_id from user where telegram_id={telegram_id}), "{event_id}")
            """
    try:
        with connection:
            cursor.execute(cancel_script)
        print(cursor.lastrowid)
        # result = cursor.
        return result

    except Error as e:
        print(f"The error '{e}' occurred")


def delete_event(telegram_id, club_id, event_id):
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    cancel_script = f"""
DELETE FROM event
WHERE club_id={club_id} and event_id={event_id}
            """
    try:
        with connection:
            cursor.execute(cancel_script)
        print(cursor.lastrowid)
        # result = cursor.
        return result

    except Error as e:
        print(f"The error '{e}' occurred")

# Создание регистрируемого пользователя после получения информации об имени
def create_user(message):  # По идее, универсальная функция под update, insert
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    registration_script = f"""
            INSERT INTO User (telegram_id, name)
            VALUES ("{message.from_user.id}", "{message.text}")
            """
    try:
        with connection:
            cursor.execute(registration_script)
        print(cursor.lastrowid)
        # result = cursor.
        return result

    except Error as e:
        print(f"The error '{e}' occurred")


def create_user_rank(callbackdata, telegram_id):
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    registration_script = f"""
        INSERT INTO user_rank (user_id, rank_id)
        VALUES ((select user_id from user WHERE telegram_id='{telegram_id}'), (SELECT rank_id from rank where rank_name='new_bro' and club_id={callbackdata.data[5:]}))
        """
    print(registration_script)
    try:
        with connection:
            cursor.execute(registration_script)
        print(cursor.lastrowid)
        # result = cursor.
        return result

    except Error as e:
        print(f"The error '{e}' occurred")


def update_rank(user_id, club_id, rank_name):
    connection = create_connection(DataBasePath)
    script = f'''
    update user_rank
    set rank_id = (
    select rank_id from rank where club_id='{club_id}' and rank_name='{rank_name}')
    where user_id={user_id}
    '''
    print(script)
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(script)
            result = cursor.fetchall()
            return result
            print(result)
    except Error as e:
        print(f"The error '{e}' occurred")
    print(result)

def update_place_new_event(callback_data):
    connection = create_connection(DataBasePath)
    print("place_id", callback_data.data.split("/")[1])
    print("event_id", callback_data.data.split("/")[2])
    script = f'''
    update event
    set place_id = {callback_data.data.split("/")[1]}
    where event_id = {callback_data.data.split("/")[2]}
    
        '''
    print(script)
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(script)
            result = cursor.fetchall()
            return result
            print(result)
    except Error as e:
        print(f"The error '{e}' occurred")

# Универсальный скрипт для обновления таблицы user
def update_user(TI, surname=None, phone=None, car_info=None, email=None):
    text = """update user
              SET \n"""
    if surname != None:
        text += f"""surname='{surname}'"""
    if phone != None:
        text += f"""phone='{phone}'"""
    if car_info != None:
        text += f"""car_info='{car_info}'"""
    if email != None:
        text += f"""email='{email}'"""
    text += f"""\nWHERE telegram_id='{TI}'"""
    print(text)
    connection = create_connection(DataBasePath)
    cursor = connection.cursor()
    result = None
    try:
        with connection:
            cursor.execute(text)
        print(cursor.lastrowid)
        # result = cursor.
        return result

    except Error as e:
        print(f"The error '{e}' occurred")



# Запрос клубов, в которых не состоит участник

# SELECT * from club
def get_club():
    connection = create_connection(DataBasePath)
    script = f'''SELECT club_id, club_name from club'''
    cursor = connection.cursor()
    club_list = None
    try:
        cursor.execute(script)
        club_list = cursor.fetchall()
        return club_list
    except Error as e:
        print(f"The error '{e}' occurred")


def category_list():
    connection = create_connection(DataBasePath)
    script = f'''SELECT * from category'''
    cursor = connection.cursor()
    category_list = None
    try:
        cursor.execute(script)
        category_list = cursor.fetchall()
        return category_list
    except Error as e:
        print(f"The error '{e}' occurred")


def get_new_bro_list(club_id):
    connection = create_connection(DataBasePath)
    script = f'''
SELECT user_id, name, surname, phone, telegram_id
from user_rank
inner join rank using (rank_id)
INNER JOIN user USING (user_id)
WHERE rank_name="new_bro" and club_id={club_id}
'''
    cursor = connection.cursor()
    new_bro_list = None
    try:
        cursor.execute(script)
        new_bro_list = cursor.fetchall()
        return new_bro_list
    except Error as e:
        print(f"The error '{e}' occurred")


def get_trener_list(club_id):
    connection = create_connection(DataBasePath)
    script = f'''
SELECT telegram_id
FROM user
inner JOIN user_rank USING (user_id)
inner JOIN rank USING (rank_id)
where rank_name in ("trener", "admin") and club_id={club_id}
'''
    cursor = connection.cursor()
    trener_list = None
    try:
        cursor.execute(script)
        trener_list = cursor.fetchall()
        return trener_list
    except Error as e:
        print(f"The error '{e}' occurred")


def get_trener_list_for_event(event_id):
    connection = create_connection(DataBasePath)
    print("get_trener_list_for_event", event_id)
    script = f'''
SELECT name, surname, user_id, event_id
from user
inner join user_rank USING (user_id)
inner join rank USING (rank_id)
INNER join club USING (club_id)
inner join event using (club_id)
WHERE event_id={event_id} AND rank_name in ("trener", "admin")
'''
    print(script)
    cursor = connection.cursor()
    trener_event_list = None
    try:
        cursor.execute(script)
        trener_event_list = cursor.fetchall()
        return trener_event_list
    except Error as e:
        print(f"The error '{e}' occurred")
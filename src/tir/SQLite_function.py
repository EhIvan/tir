# Файл для работы с БД


import sqlite3
from sqlite3 import Error


# Путь к БД
#DataBasePath = "C:\\Users\\79175\\Documents\\GitHub\\tir\\src\\tir_db\\tir_db.db"  # Адрес старой БД
#DataBasePath = "C:\\Users\\79175\\Documents\\GitHub\\tir\\src\\TIRDB.db"  # Адрес БД


DataBasePath = f"../TIRDB"  # Относительный адрес БД

# Функция соединения с БД

def create_connection(DataBasePath):  # Подключение к БД
    connection = None
    try:
        connection = sqlite3.connect(DataBasePath)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


#
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

def update_user(TI, surname=None, mobile=None, car_info=None, email=None):  # По идее, универсальная функция под update, insert


    text = """update user
              SET \n"""
    if surname != None:
        text += f"""surname='{surname}'"""
    if mobile != None:
        text += f"""mobile='{mobile}'"""
    if car_info != None:
        text += f"""mobile='{car_info}'"""
    if email != None:
        text += f"""mobile='{email}'"""
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





#get_rank(create_connection(DataBasePath), 15978)







# Функции для определения ранга пользователя

def check_rank(user_id):  # Тянет из БД ранг стрелка: админ, тренер, стрелок
    check_rank = f"""
    select rank_name from
    rank
    inner join user using (rank_id)
    where telegram_id='{user_id}'
    """
    return check_rank


# Функция SELECT из БД

def execute_read_query(connection, query):  # По идее, универсальная функция под SELECT
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
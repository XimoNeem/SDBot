# import pymysql
import sqlite3
from typing import List

from scripts.bot_config import * 
from scripts.bot_types import ProductType
import scripts.bot_items

connection = sqlite3.connect(scripts.bot_config.config_databasePath, check_same_thread=False)
cursor = connection.cursor()

def get_user(user_id: int):
    '''
    Get user from db
    '''
    print(f'[LOG] Get user with id {user_id}')

    cursor.execute(f'''SELECT * FROM userData WHERE user_id = {user_id}''')
    user_data = cursor.fetchone()
    if user_data is None:
        print('[WARNING] No such user')
        return None
    else:
        user = scripts.bot_items.User(
                user_id= user_data[2],
                user_name= user_data[3],
                user_nickname=user_data[4],
                user_tockens=user_data[6]
            )    
        return user

def create_user(user):
    '''
    Add new user to db
    '''
    try:
        user_data = cursor.execute('SELECT * FROM userData WHERE user_id = ?', (user.id, ))
        if user_data.fetchone() is None:
            cursor.execute('''INSERT INTO userData (user_id, user_nickname, user_name) VALUES (?, ?, ?)''', (user.id, user.username, user.first_name))
            connection.commit()
            print(f'[LOG] Пользователь с id {user.id} добавлен в базу')
        else:
            print(f'[WARNING] Пользователь с id {user.id} уже в базе')
    except sqlite3.Error as error:
        print('[ERROR] Cant add new user to database > ' + error)

def set_currentPage(user_id:int, page_id):
    '''
    Update current users page
    '''
    cursor.execute(f"""UPDATE userData SET user_currentPageId = "{page_id}" where user_id = {user_id}""")
    connection.commit()

def get_currentPageId(user_id:int) ->str:
    try:
        cursor.execute(f'''SELECT user_currentPageId FROM userData WHERE user_id = {user_id}''')
        return str(cursor.fetchone()[0])
    except sqlite3.Error as error:
        print('[ERROR] Ошибка при получении списка сообщений из sqlite: ', error)
        return 'welcome'

def get_user_tockens(user_id:int):
    try:
        cursor.execute(f'''SELECT user_tockens FROM userData WHERE user_id = {user_id}''')
        return int(cursor.fetchone()[0])
    except sqlite3.Error as error:
        print('[ERROR] Ошибка при получении списка сообщений из sqlite: ', error)
        return 0
    
def set_user_tockens(user_id:int, value:int):
    try:
        cursor.execute(f"""UPDATE userData SET user_tockens = {value} where user_id = {user_id}""")
        connection.commit()
    except sqlite3.Error as error:
        print('[ERROR] Ошибка при добавлении токенов sqlite: ', error)
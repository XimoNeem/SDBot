# import bot_config
# import sqlite3
# import pymysql

# try:
#     connection = pymysql.connect(
#         host=bot_config.config_mysqlhost,
#         user = bot_config.config_mysquser,
#         password=bot_config.config_mysqpassword,
#         database=bot_config.config_databaseName,
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print('Y')
# except pymysql.Error as error:
#     print(error)

# # connection = sqlite3.connect('https://www.pythonanywhere.com/user/xem/files/home/xem/bot/database.db', check_same_thread=True)


from bot_config import config_requestUrl
import requests

payload = {
    "prompt": "maltese puppy",
    "steps": 5
}

try:
    response = requests.post(url=config_requestUrl, json=payload)
    result = response.json()
    print(result)
except:
    print('Error')

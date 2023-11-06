import scripts.bot_db_handler

from typing import List
from scripts.bot_types import ProductType
from telebot import types, TeleBot
from scripts.bot_messages import *


class BotPage:
    def __init__(self, page_text: str, page_id: str, page_markup: list[tuple]=None, page_image: str=None, page_parent: str = 'welcome', call_back:str = ''):
        self.page_id = page_id
        self.text= page_text
        self.imageURL = page_image
        self.reply_markup = None
        if page_markup is not None:
            keyboard = []
            for row in page_markup:
                row_buttons = []
                for item in row:
                    row_buttons.append(types.InlineKeyboardButton(text=str(item), callback_data=f'{call_back}{str(item)}'))
                keyboard.append(row_buttons)
            
            self.reply_markup = types.InlineKeyboardMarkup(keyboard)

        self.parent:str = page_parent

class User:
    '''
    Bot user
    '''
    def __init__(self, user_id:int, user_name:str, user_nickname:str, user_tockens:int):
        self.id = user_id
        self.name = user_name
        self.nickname = user_nickname
        self.tockens = user_tockens

    def subtract_tocken(self):
        self.tockens -= 1
        scripts.bot_db_handler.set_user_tockens(self.id, self.tockens)
    
    def print_data(self):
        print(f'[LOG] user data -> [{self.id}] [{self.name}] [{self.nickname}] [{self.tockens}]')
    
    def add_token(self, value:int):
        self.tockens += value
        scripts.bot_db_handler.set_user_tockens(self.id, self.tockens)
        
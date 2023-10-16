from scripts.bot_pages import *
import asyncio

import requests

import scripts.bot_db_handler

async def draw_image(user_id:int, promt:str, action_onFailure, action_arg1, action_arg2) -> str:
    user = scripts.bot_db_handler.get_user(user_id)
    if user.tockens < 1:
        await action_onFailure(user_id, action_arg1)
        await action_onFailure(user_id, action_arg2)
        return None
    else:
        user.subtract_tocken()

        url = 'https://www.w3schools.com/python/demopage.php'
        data = {'somekey': 'somevalue'}
        result = requests.post(url, json = data)
        print(result.text)

        return 'https://i0.wp.com/learn.onemonth.com/wp-content/uploads/2017/08/1-10.png?w=845&ssl=1'
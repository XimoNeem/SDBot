from scripts.bot_db_handler import *

#TODO payments...

def check_payment(user_id:int) -> bool:
    #TODO payment check...

    user = get_user(user_id)
    user.add_token(1)

    return True
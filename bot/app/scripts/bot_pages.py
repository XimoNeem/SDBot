from telebot import types
from scripts.bot_items import *
from scripts.bot_messages import *
from scripts.bot_db_handler import get_user_tockens

basePages = {
'welcome' : BotPage(message_welcome, 'welcome', ((button_draw, ), (button_account, ), (button_pay, button_info))),
'finishPay' : BotPage(message_payFinised, 'payFin', ((button_back, ),)),
'rateRequest' : BotPage(message_rate, 'rate'),
'toCheckout' : BotPage(message_toCheckOut, 'toCheckout', ((button_pay, ), (button_cancel,),)),
'onError' : BotPage(message_error, 'error', ((button_back, ),)),
}

def get_page(page_id:str) -> BotPage:
    try: return basePages[page_id]
    except Exception as e: print(e)

#Extra pages

def get_account_page(user) -> BotPage:
    text = message_accouunt.format(user.first_name, user.id, get_user_tockens(user.id))
    return BotPage(text, 'account', ( (button_cancel, ),))

def get_pay_page(user) -> BotPage:
    # text = message_pay.format('https://web.telegram.org/a/#6683897220')
    text = message_pay.format('ссылка')
    return BotPage(text, 'pay', ( (button_confirmPay,),  (button_cancel,) ))

def get_image_page(user, image_url:str) -> BotPage:
    return BotPage('', 'drawFinished', page_image=image_url, page_markup= ( (button_rate, ), ))

def get_draw_page(user):
    page = BotPage(message_draw, 'draw', prompt_options, call_back='prompt_')
    page.reply_markup.add(types.InlineKeyboardButton(text=button_resume, callback_data=button_resume))
    page.reply_markup.add(types.InlineKeyboardButton(text=button_back, callback_data=button_back))
    return page
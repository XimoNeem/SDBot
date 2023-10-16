import asyncio
import telebot.types


from scripts.bot_pay_system import check_payment
from telebot.async_telebot import AsyncTeleBot
from scripts import bot_config
from scripts.bot_items import *
from scripts.bot_types import *
# from scripts.bot_db_handler import *
from scripts.bot_pages import *
from scripts.bot_messages import *
from scripts.bot_db_handler import *
from scripts.bot_drawer import draw_image


bot = AsyncTeleBot(bot_config.config_token)

@bot.message_handler(commands=['start'])
async def command_start(message):
	await bot.delete_message(message.chat.id, message.message_id)
	await show_page(message.from_user.id, get_page('welcome'))

	user = get_user(message.from_user.id)
	if user is None: create_user(message.from_user)
	else: user.print_data()
	

@bot.message_handler(content_types= ['text'])
async def command_start(message):
	if get_currentPageId(message.from_user.id) == 'draw':
		failure_page1 = get_page('welcome')
		failure_page2 = get_page('toCheckout')
		imageURL = await draw_image(message.from_user.id, 'girl', show_page, failure_page1, failure_page2)
		await bot.delete_message(message.chat.id, message.message_id - 1)
		await bot.delete_message(message.chat.id, message.message_id)
		if not imageURL == None:
			await show_page(message.from_user.id, get_image_page(message.from_user, imageURL))
			await show_page(message.from_user.id, get_page('welcome'))
	await bot.delete_message(message.chat.id, message.message_id)

async def show_page(user_id, page: BotPage):
	print(f'[LOG] show page [{str(page.page_id)}]')
	set_currentPage(user_id, page.page_id)
	if page.imageURL is None:
		await bot.send_message(user_id, page.text, reply_markup = page.reply_markup, parse_mode="Markdown")
	else:
		# img = open(page.imageURL, 'rb')
		await bot.send_photo(user_id, page.imageURL, caption = page.text, reply_markup = page.reply_markup, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
async def check_callback(call):
	if call.data == button_back: 
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await show_page(call.from_user.id, get_page('welcome'))
	elif call.data == button_cancel: await bot.delete_message(call.message.chat.id, call.message.message_id)
	elif call.data == button_draw:
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await show_page(call.from_user.id, get_page('draw'))
	elif call.data == button_account: await show_page(call.from_user.id, get_account_page(call.from_user))
	elif call.data == button_pay: await show_page(call.from_user.id, get_pay_page(call.from_user))
	elif call.data == button_confirmPay: 
		if check_payment(call.from_user.id):
			await bot.answer_callback_query(call.id, message_payFinised, show_alert=True)
			await bot.delete_message(call.message.chat.id, call.message.message_id)

	elif call.data == button_rate:
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton(text=button_rate0, callback_data='setRate'),
					types.InlineKeyboardButton(text=button_rate1, callback_data='setRate'),
					types.InlineKeyboardButton(text=button_rate2, callback_data='setRate'),
					types.InlineKeyboardButton(text=button_rate3, callback_data='setRate'),
					types.InlineKeyboardButton(text=button_rate4, callback_data='setRate')
		)
		await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = markup)

	elif call.data == 'setRate':
		await bot.answer_callback_query(call.id, warning_finishRate, show_alert=True)
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton(text=button_rate, callback_data=button_rate))
		await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = markup)
		# await show_page(call.from_user.id, get_page('welcome'))

	elif call.data == button_info:
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton(text=button_infoAdmin, url='https://web.telegram.org/a/#6683897220'))
		markup.add(types.InlineKeyboardButton(text=button_cancel, callback_data=button_cancel))
		await bot.send_message(call.message.chat.id, message_info, reply_markup = markup, parse_mode="Markdown")


if __name__ == '__main__':
    asyncio.run(bot.polling())
import telepot
import time
import json
from pprint import pprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def handle(msg_detail):
    pprint(msg_detail)
    
def on_chat_message(msg):
    
    print(telepot.flavor(msg))
    
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='press')],
                   [InlineKeyboardButton(text='Press me', callback_data='hello')]
               ])

    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

def on_callback_query(msg):
    
    print(telepot.flavor(msg))
    
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


if __name__ == '__main__':
    
    with open ('Token.json', 'r') as json_file:
        data = json.load(json_file)
    TOKEN = data['token']
    
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, {'chat': on_chat_message,
                      'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')
    
    while 1:
        time.sleep(10)
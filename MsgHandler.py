#%%
import json
import time
import logging
import telegram
from pprint import pprint
from telegram import Update
from telegram.ext import CallbackContext

#%%
logger = logging.getLogger(__name__)

#%%
def start_command(update: Update, context: CallbackContext):
    
    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    re_msg = '這是專門用來追蹤商品價格的機器人\n會在特價時通知你'
    update.message.reply_text(re_msg)
    
    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    context.match()
    
    re_msg = '目前僅支援24pchome和momo喔\n現在先嘗試加入一個商品頁面的網址看看吧\n/add https://xxxxxx'
    update.message.reply_text(re_msg)
    
#%%
def help_command(update: Update, context: CallbackContext):
    
    re_msg = '此機器人是來嘸蝦米查碼的喔\n僅只援繁體中文'
    update.message.reply_text(re_msg)
    
#%%
def add_command(update: Update, context: CallbackContext):
    
    re_msg = '此機器人是來嘸蝦米查碼的喔\n僅只援繁體中文'
    update.message.reply_text(re_msg)
    
#%%
def del_command(update: Update, context: CallbackContext):
    
    re_msg = '此機器人是來嘸蝦米查碼的喔\n僅只援繁體中文'
    update.message.reply_text(re_msg)
    
#%%
def list_command(update: Update, context: CallbackContext):
    
    re_msg = '此機器人是來嘸蝦米查碼的喔\n僅只援繁體中文'
    update.message.reply_text(re_msg)
    
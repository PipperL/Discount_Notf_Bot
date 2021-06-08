#%%
import json
import time
import logging
import telegram
from pprint import pprint
from telegram import Update, MessageEntity, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from CmdHandler import CmdHandler

#%%
logger = logging.getLogger(__name__)

#%%
def start_cmd(update: Update, context: CallbackContext):
    
    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    re_msg = '這是專門用來追蹤商品價格的機器人\n會在特價時通知你'
    update.message.reply_text(re_msg)
    
    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    re_msg = '目前僅支援24pchome和momo喔\n現在先嘗試加入一個商品頁面的網址看看吧\n/add https://xxxxxx'
    update.message.reply_text(re_msg)
    
#%%
def help_cmd(update: Update, context: CallbackContext):
    
    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    re_msgs = [None] * 2
    re_msgs[0] ='/add 用來新增商品頁面\n'
    re_msgs[0] += '/del 用來刪除追蹤的商品頁面\n'
    re_msgs[0] += '/list 會列出所有的商品\n'
    re_msgs[0] += '若想看更多細項請 /help add or del or list'
    
    msg_sep = update.message.text.split(' ')
    if len(msg_sep) >= 2:
        if msg_sep[1] == 'add':
            re_msgs[0] = '範例: /add https://24h.pchome.com.tw/prod/DCAYKO-A90090S6A'
            
        elif msg_sep[1] == 'del':
            re_msgs[0] = '範例: /del 耳機\n'
            re_msgs[0] += '這樣就會把所有商品名稱中包含耳機的全部刪掉喔'
            re_msgs[1] = '如果忘了自己到底加了什麼\n'
            re_msgs[1] += '那就直接 /del 就會列出來囉'
            
        elif msg_sep[1] == 'list':
            re_msgs[0] = '範例: /list\n'
            re_msgs[0] += '就會自動列出囉'
            re_msgs[1] = '如果想針對電商進行查詢\n'
            re_msgs[1] += '那就 /list 24pchome or momo'
            
    for msg in re_msgs:
        if msg: 
            update.message.reply_text(msg)
    
#%%
def add_cmd(update: Update, context: CallbackContext):
    
    #markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton('pre', callback_data='help test')]], )
    
    add_url = update.message.text.split()[1]
    if 'https:' in add_url:
        add_handle = CmdHandler(update.message.chat_id, url=add_url)
        
        
    re_msg = '成功加入囉'
    update.message.reply_text(re_msg)
    
#%%
def del_cmd(update: Update, context: CallbackContext):
    
    re_msg = ' '
    update.message.reply_text(re_msg)
    
#%%
def list_cmd(update: Update, context: CallbackContext):
    
    re_msg = ' '
    update.message.reply_text(re_msg)

#%%
def msg_exp(update, context):
    
    pass
#%%
import time
import logging
import telegram
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from CmdHandler import CmdHandler


logger = logging.getLogger(__name__)


def start_cmd(update: Update, context: CallbackContext):

    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    re_msg = '這是專門用來追蹤商品價格的機器人\n會在特價時通知你\n/help 看更多資訊'
    update.message.reply_text(re_msg)
    
    context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    
    re_msg = '目前僅支援24pchome和momo喔\n現在先嘗試加入一個商品頁面的網址看看吧\n/add https://xxxxxx'
    update.message.reply_text(re_msg)
    

def help_cmd(update: Update, context: CallbackContext):
    
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(1)
    msg_sep = update.message.text.split(' ')
    re_msgs = [None] * 2
    
    if len(msg_sep) == 1:
        markup = telegram.InlineKeyboardMarkup(
            [[telegram.InlineKeyboardButton('電商歷史價格查詢', url='https://twbuyer.info/')]]
            )
        
        re_msg = '首先 先用這個查查歷史最低價來決定要不要等特價吧\n'
        update.message.reply_text(re_msg, reply_markup=markup)
        
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(1)
        
        re_msg = '若確定要等請看下面\n/add 用來新增商品頁面\n'
        re_msg += '/del 用來刪除追蹤的商品頁面\n'
        re_msg += '/list 會列出所有的商品\n'
        re_msg += '若想看更多細項請 /help add / del / list'
        update.message.reply_text(re_msg)
        
    elif len(msg_sep) >= 2:
        if msg_sep[1] == 'add':
            re_msgs[0] = '範例: /add https://24h.pchome.com.tw/prod/DCAYKO-A90090S6A'
            
        elif msg_sep[1] == 'del':
            re_msgs[0] = '範例: /del 耳機\n'
            re_msgs[0] += '這樣就會把所有商品名稱中包含耳機的全部刪掉喔'
            re_msgs[1] = '如果忘了自己到底加了什麼\n'
            re_msgs[1] += '那就直接 /del 就會列出來囉\n'
            re_msgs[1] += '接著點選就會刪除了'
            
        elif msg_sep[1] == 'list':
            re_msgs[0] = '範例: /list\n'
            re_msgs[0] += '就會自動列出囉'
            
        for msg in re_msgs:
            if msg: 
                update.message.reply_text(msg)


def add_cmd(update: Update, context: CallbackContext):
    
    update.message.reply_text('請稍等')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    
    try:
        add_new_url = update.message.text.split()[1]
        if 'https:' in add_new_url:
            add_handle = CmdHandler(update.message.chat_id, url=add_new_url)
            re_msg = add_handle.add_url()
    
    except IndexError:
        re_msg = '記得加上商品網址喔'
    
    update.message.reply_markdown_v2(re_msg, disable_web_page_preview=True)
    

def del_cmd(update: Update, context: CallbackContext):

    del_keyword = update.message.text.split()
    if len(del_keyword) == 1:
        # InlineKeyboard
        # reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton('momo', callback_data='del momo'),
        #                                                telegram.InlineKeyboardButton('pchome', callback_data='del pchome')]], )
        # re_msg = '請問想要刪掉哪間電商的追蹤商品呢？'
        # update.message.reply_text(re_msg, reply_markup=reply_markup)
        re_msg = '請在 /del 後輸入想刪掉的商品關鍵字'

    elif len(del_keyword) == 2:
        del_keyword = del_keyword[1]
        logger.info(f'will del {del_keyword}')
        del_handle = CmdHandler(update.message.chat_id, keyword=del_keyword)
        re_msg = del_handle.del_by_keyword()

    update.message.reply_text(re_msg)

    #context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)


def list_cmd(update: Update, context: CallbackContext):
    
    list_handle = CmdHandler(update.message.chat_id)
    pchome_re_msg, momoshop_re_msg = list_handle.prods_list()
    
    update.message.reply_markdown_v2('24hPChome:\n' + pchome_re_msg, disable_web_page_preview=True)
    update.message.reply_markdown_v2('momoshop:\n' + momoshop_re_msg, disable_web_page_preview=True)


def exp_msg(update, context):
    
    pass


def error_callback(update, context):
    
    try:
        raise context.error
        
    except Exception as e:
        logger.error(e)

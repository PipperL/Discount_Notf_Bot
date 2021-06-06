#%%
import json
import logging
from telegram import Update
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackContext
from MsgHandler import *

#%%
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#%%
if __name__ == '__main__':
    
    with open ('Token.json', 'r') as json_file:
        data = json.load(json_file)
    TOKEN = data['token']
    
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    # Command
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('add', add_command))
    dispatcher.add_handler(CommandHandler('del', del_command))
    dispatcher.add_handler(CommandHandler('list', list_command))
    
    updater.start_polling()
    logger.info('Listening')
    
    updater.idle()
#%%
import json
import logging
from telegram import Update
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackContext
from MsgHandler import start_cmd, help_cmd, add_cmd, del_cmd, list_cmd, msg_exp

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
    
    # ignore edit
    dispatcher.add_handler(MessageHandler(Filters.update.edited_message, msg_exp))
    
    # Command
    dispatcher.add_handler(CommandHandler('start', start_cmd))
    dispatcher.add_handler(CommandHandler('help', help_cmd))
    dispatcher.add_handler(CommandHandler('add', add_cmd))
    dispatcher.add_handler(CommandHandler('del', del_cmd))
    dispatcher.add_handler(CommandHandler('list', list_cmd))
    
    updater.start_polling()
    logger.info('Listening')
    
    updater.idle()
    
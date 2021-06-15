#%%
import os
import json
import logging
import time
from Notification import NotifyThread
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from MsgReplyer import start_cmd, help_cmd, add_cmd, del_cmd, list_cmd, exp_msg, error_callback

#%%
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logger.log',
                    filemode='w',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#%%
if __name__ == '__main__':
    
    with open('Token.json', 'r') as json_file:
        data = json.load(json_file)
    TOKEN = data['token']
    
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    # ignore edit
    dispatcher.add_handler(MessageHandler(Filters.update.edited_message, exp_msg))
    
    # Command
    dispatcher.add_handler(CommandHandler('start', start_cmd))
    dispatcher.add_handler(CommandHandler('help', help_cmd))
    # dispatcher.add_handler(CommandHandler('add', add_cmd))
    dispatcher.add_handler(CommandHandler('del', del_cmd))
    dispatcher.add_handler(CommandHandler('list', list_cmd))

    dispatcher.add_handler(MessageHandler(Filters.text
                                          & (Filters.entity('url'))
                                          & ~Filters.command, add_cmd))

    dispatcher.add_handler(MessageHandler(~Filters.command & ~Filters.text, exp_msg))
    dispatcher.add_handler(MessageHandler(Filters.text, exp_msg))
    # dispatcher.add_error_handler(error_callback)
    
    updater.start_polling()
    logger.info('Listening')

    # path = './json'
    # while True:
    #     json_files = os.listdir(path)
    #     for file in json_files:
    #         user_data_path = os.path.join(path, file)
    #         NotifyThread(dispatcher, user_data_path).start()
    #
    #     time.sleep(7200)

    updater.idle()

#%%
import os
import logging
import requests
import json

#%%
logger = logging.getLogger(__name__)

#%%
class CmdHandler:

    def __init__(self, chat_id, text=None, url=None):
        
        self.chat_id = chat_id
        self.text = text
        self.url = url
        self.prods = list()
        
        # Check if the json/ exists
        try:
            os.mkdir('./json')
        
        except FileExistsError:
            pass
        
        # Check if the user file exists
        try:
            path = './json/' + str(self.chat_id) + '.json'
            with open (path, 'r') as json_file:
                user_data = json.load(json_file)
                self.prods = user_data['prods']
        
        except Exception:
            user_data = dict()
            user_data['chat_id'] = self.chat_id
            user_data['prods'] = list()
            with open (path, 'w') as json_file:
                json.dump(user_data, json_file)
            
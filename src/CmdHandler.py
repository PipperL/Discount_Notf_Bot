#%%
import os
import logging
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ECommHandler import ECommHandler

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
            with open(path, 'r') as json_file:
                self.user_data = json.load(json_file)
                self.prods = self.user_data['prods']
        
        except Exception:
            self.user_data = dict()
            self.user_data['chat_id'] = self.chat_id
            self.user_data['prods'] = list()
            with open(path, 'w') as json_file:
                json.dump(self.user_data, json_file)
    
    #%%
    def add_url(self):
        
        for prod in self.prods:
            if self.url == prod['url']:
                re_msg = '這個網址已經在追蹤列表裡囉'
                return re_msg
        
        if '24h.pchome' and 'prod' in self.url:              
            prod_name, prod_price = ECommHandler(self.url).pchome()
                
        elif 'momoshop' and 'goods' in self.url:
            print(self.url)
            prod_name, prod_price = ECommHandler(self.url).momoshop()
            
        else:
            re_msg = '請貼 24pchome 或是 momo 的 商品頁面 喔'
            return re_msg
        
        self.prods.append({'name': prod_name, 
                           'price': prod_price,
                           'url': self.url})
        self.user_data['prods'] = self.prods
        
        path = './json/' + str(self.chat_id) + '.json'
        with open(path, 'w') as json_file:
            json.dump(self.user_data, json_file)
        
        re_msg = prod_name + ' 已成功加入囉'
        return re_msg
#%%
import re
import os
import logging
import json
from ECommHandler import ECommHandler

#%%
logger = logging.getLogger(__name__)

#%%
class CmdHandler:

    def __init__(self, chat_id, keyword=None, url=None):
        
        self.chat_id = chat_id
        self.keyword = keyword
        self.url = url
        self.prods = list()
        
        # Check if the json/ exists
        try:
            os.mkdir('./json')
        
        except FileExistsError:
            pass

        # dill with url
        if self.url:
            self.get_fixed_type_url()

        # Check if the user file exists
        path = './json/' + str(self.chat_id) + '.json'
        try:
            with open(path, 'r') as json_file:
                self.user_data = json.load(json_file)
                self.prods = self.user_data['prods']
        
        except Exception:
            self.user_data = dict()
            self.user_data['chat_id'] = self.chat_id
            self.user_data['prods'] = list()
            with open(path, 'w') as json_file:
                json.dump(self.user_data, json_file)

    def get_fixed_type_url(self):

        if 'pchome' in self.url:
            self.url = self.url.replace('24h.m.pchome', '24h.pchome')
            self.url = re.split('\?', self.url)[0]

        elif 'momoshop' in self.url:

            momo_basic_url = 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?'
            url_split = re.split('\?|&', self.url)

            for url_part in url_split:
                if 'i_code=' in url_part:
                    i_code = url_part
                    self.url = momo_basic_url + i_code
                    break

    def add_url(self):

        if len(self.prods) >= 10:
            re_msg = '你已加入十個商品囉'
            return re_msg

        for prod in self.prods:
            if self.url == prod['url']:
                re_msg = '這個網址已經在追蹤列表裡囉'
                return re_msg
        
        if '24h.pchome' and 'prod' in self.url:              
            prod_name, prod_price = ECommHandler(self.url).pchome()
            ecomm_store = '24hpchome'
                
        elif 'momoshop' and 'goods' in self.url:
            prod_name, prod_price = ECommHandler(self.url).momoshop()
            ecomm_store = 'momoshop'
            
        else:
            re_msg = '請貼 24pchome 或是 momo 的 商品頁面 喔'
            return re_msg
        
        replace_list = ['-', '(', ')', '[', ']', '+', '.', '|', '_']
        for c in replace_list:
            prod_name = prod_name.replace(c, '\\' + c)
        
        self.prods.append({'name': prod_name,
                           'store': ecomm_store,
                           'price': prod_price,
                           'url': self.url})

        self.write_back()
        
        re_msg = prod_name + ' 已成功加入囉'
        return re_msg

    def prods_list(self):
        
        pchome_list = list()
        momoshop_list = list()
        pchome_msg = ''
        momoshop_msg = ''
        
        for prod in self.prods:
            if prod['store'] == '24hpchome':
                pchome_list.append('[' + prod['name'] + '](' + prod['url'] + ')')
            
            elif prod['store'] == 'momoshop':
                momoshop_list.append('[' + prod['name'] + '](' + prod['url'] + ')')

        for i, link_text in enumerate(pchome_list):
            pchome_msg += link_text
            
            if i != len(pchome_list)-1:
                pchome_msg += '\n'
        
        for i, link_text in enumerate(momoshop_list):
            momoshop_msg += link_text
            
            if i != len(momoshop_list)-1:
                momoshop_msg += '\n'

        return pchome_msg, momoshop_msg

    def del_by_keyword(self):

        num_del = 0
        self.keyword = self.keyword.lower()
        for i, prod in enumerate(self.prods):
            if self.keyword in prod['name'].lower():
                del self.prods[i]
                num_del += 1

        if num_del:
            self.write_back()
            re_msg = f'已刪除 {num_del} 項追蹤商品'
        else:
            re_msg = '追蹤商品中並沒有包含此關鍵字的商品喔'
        return re_msg

    def write_back(self):

        self.user_data['prods'] = self.prods

        path = './json/' + str(self.chat_id) + '.json'
        with open(path, 'w') as json_file:
            json.dump(self.user_data, json_file)

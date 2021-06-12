import threading
import json
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


class NotifyThread(threading.Thread):

    def __init__(self, dispatcher, user_data_path):

        threading.Thread.__init__(self)

        self.dispatcher = dispatcher

        with open(user_data_path, 'r') as json_file:
            self.user_data = json.load(json_file)

        self.chat_id = self.user_data['chat_id']

        opts = Options()
        opts.headless = True
        self.driver = webdriver.Firefox(firefox_options=opts)
        self.WebWait = WebDriverWait(self.driver, 20)

    def run(self) -> None:

        logger.info(threading.currentThread().name + ' start working')

        for prod in self.user_data['prods']:

            new_prod_price = self.get_new_price(prod['url'])

            if new_prod_price < prod['price']:
                prod['price'] = new_prod_price
                context = CallbackContext(self.dispatcher)
                re_msg = '[' + prod['name']+']' \
                         + '(' + prod['url'] + ')' \
                         + ' 現在特價 ' + str(prod['price']) + '元'
                context.bot.send_message(self.chat_id, re_msg, parse_mode='MarkdownV2')

            elif new_prod_price > prod['price']:
                prod['price'] = new_prod_price

        self.driver.quit()
        self.write_back()
        logger.info(threading.currentThread().name + ' finish work')

    def get_new_price(self, url):

        self.driver.get(url)
        try:
            if '24h.pchome' in url:
                new_prod_price = self.WebWait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//span[@class='price']/span[@id='PriceTotal']")
                    )
                ).text

            elif 'momoshop' in url:
                new_prod_price = self.WebWait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//li[@class='special']/span")
                    )
                ).text
                new_prod_price = new_prod_price.replace(',', '')

            new_prod_price = int(new_prod_price)

        except Exception:
            logger.info(url + ' not found')

        return new_prod_price

    def write_back(self):

        path = './json/' + str(self.chat_id) + '.json'
        with open(path, 'w') as json_file:
            json.dump(self.user_data, json_file)

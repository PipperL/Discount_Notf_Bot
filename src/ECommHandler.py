#%%
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException

#%%
logger = logging.getLogger(__name__)


class ECommHandler:
    
    def __init__(self, url):
        opts = Options()
        opts.headless = True
        self.driver = webdriver.Firefox(firefox_options=opts)
        self.WebWait = WebDriverWait(self.driver, 20)
        self.url = url

    #%%
    def pchome(self):

        try:
            self.driver.get(self.url)

        except InvalidArgumentException:
            return None, None

        try:
            prod_name = self.WebWait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h3[@class='prod_name']/span[@itemprop='name']")
                    ) 
                ).text
    
            prod_price = self.WebWait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[@class='price']/span[@id='PriceTotal']")
                    )
                ).text
    
        except:
            logger.info('still not found')
        
        self.driver.quit()
        logger.info('pchome selenium success')
        return prod_name, int(prod_price)
    
    #%%
    def momoshop(self):

        try:
            self.driver.get(self.url)

        except InvalidArgumentException:
            return None, None

        try:
            prod_name = self.WebWait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='prdnoteArea']/h3")
                    )
                ).text

            prod_price = self.WebWait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//li[@class='special']/span")
                    )
                ).text
            prod_price = prod_price.replace(',', '')
            
        except:
            logger.info('still not found')
        
        self.driver.quit()
        logger.info('momo selenium success')
        return prod_name, int(prod_price)


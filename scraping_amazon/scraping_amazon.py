from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os
import sys 

sys.path.append('scraping_amazon')

import personaldata

s = Service("./geckodriver")
o = Options()
o.add_argument("-profile")
o.add_argument(personaldata.profile)
o.headless = True

web = webdriver.Firefox(service=s, options=o)

time.sleep(2)

df = []

for i in range(1, 5, 1):

    web.get(f"https://www.amazon.com/s?k=cooker&page={i}")
    
    time.sleep(5)
    
    items = web.find_elements(by="xpath", value='//div[@data-component-type="s-search-result"]')
    for item in items:
        try:
            title = item.find_element(by="xpath", value='.//div[@data-cy="title-recipe"]')
            price = item.find_element(by="xpath", value='.//span[@class="a-price"]')
            rating = item.find_element(by="xpath", value='.//div[@data-cy="reviews-block"]')
            delivery = item.find_element(by="xpath", value='.//div[@data-cy="delivery-recipe"]')
            df.append({
                'title': title.text, 
                'price': '.'.join(price.text.split('\n')), 
                'rating': rating.text,
                'delivery': delivery.text
                })
            print(df[-1])
        except Exception as why:
            # print(why)
            continue
    
    print(f'Scraping page {i} finished.')
    
df = pd.DataFrame(df)
df.to_csv('scraping_amazon/result.csv')

time.sleep(3)

web.quit()














#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 09:45:43 2024

@author: saidahmad
"""

from seleniumbase import SB

with SB(uc=True) as sb:
    url = "https://app.getstake.com/"
    # url = 
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_click_captcha()


#%%

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
import numpy as np
import os
import sys 

sys.path.append('scraping_getstake')

import personaldata

s = Service("./geckodriver")
o = Options()
o.add_argument("-profile")
o.add_argument(personaldata.profile)
o.headless = True

web = webdriver.Firefox(service=s, options=o)
time.sleep(5)
web.get("https://app.getstake.com/home/properties?status=sold")
time.sleep(10)

sold_button = web.find_element(by='xpath', value='//button[@href="/home/properties?status=sold"]')
sold_button.click()

actions = ActionChains(web)

nattempt = 30
iattempt = 0
ncards = 0
finish = False

while True:
    
    # code
    
    while True:
        actions.send_keys(Keys.END).perform()
        iattempt += 1
        time.sleep(np.abs(np.random.normal(8, 4)))
        card_divs = web.find_elements(by='xpath', value='//div[@class="css-zjen6v"]')
        ncards_new = 1
        if ncards_new > ncards:
            iattempt = 0
            break
        elif iattempt >= nattempt:
            finish = True 
            break
    if finish:
        break
    
    
    
    


#%%

df = []

card_divs = web.find_elements(by='xpath', value='//div[@class="css-zjen6v"]')
ncards = len(card_divs)


for card in card_divs:
    
    # bed
    try:
        card.find_element(by='xpath', value='.//*[@aria-label="bed"]')
        type_p = card.find_element(by='xpath', value='.//p[contains(@class, "chakra-text")]')
        type_p = type_p.text + " bed"
        print('type:', type_p)
    except Exception as why:
        print('No bed.')
        type_p = card.find_element(by='xpath', value='.//p[contains(@class, "chakra-text")]')
        type_p = type_p.text
        print('type:', type_p)
    
    # exit door login
    try:
        door_svg = card.find_element(by='xpath', value='.//*[@aria-label="exit-door-login"]')
        door_p = door_svg.find_element(by='xpath', value='following-sibling::p[1]')
        # next_element = svg_element.find_element(By.XPATH, "following-sibling::*[1]")
        door_p = door_p.text
        print('door:', door_p.text)
    except Exception as why:
        print(why)
    
    # status
    try:
        status_span = card.find_element(by='xpath', value='(.//span[contains(@class, "chakra-badge")])[3]')
        status_span = status_span.text
        print(status_span)
    except Exception as why:
        print(why)
    
    # country
    try:
        country_span = card.find_element(by='xpath', value='(.//span[contains(@class, "chakra-badge")])[4]')
        country_span = country_span.text
        print(country_span)
    except Exception as why:
        print(why)
        
    
    # title
    title_h2 = card.find_element(by='xpath', value='.//h2')
    title_h2 = title_h2.text
    print('title:', title_h2)
    
    # price
    price_p = card.find_element(by='xpath', value='.//p[@class="chakra-text css-pcjqst"]')
    price_p = price_p.text
    print('price:', price_p)
    
    # n investor
    investor_p = card.find_element(by='xpath', value='.//p[@class="chakra-text css-myp306"]')
    investor_p = investor_p.text
    print('n investor:', investor_p)
    
    
    
    return_div = np.nan 
    date_div = np.nan 
    valuation_div = np.nan 
    paid_div = np.nan 
    other = np.nan
    detail_div = card.find_elements(by='xpath', value='.//div[@class="chakra-stack css-y25wms"]')
    
    n_detail = len(detail_div)
    for detail in detail_div:
        if 'Yearly investment return' in detail.text:
            return_div = detail.text.split('\n')[1]
        elif 'Funded date' in detail.text:
            date_div = detail.text.split('\n')[1]
        elif 'Current valuation' in detail.text:
            valuation_div = detail.text.split('\n')[1]
        elif 'Total rent paid' in detail.text:
            paid_div = detail.text.split('\n')[1]
        else:
            other = detail.text
    
    # return_div = card.find_element(by='xpath', value='.//div[@class="chakra-stack css-y25wms"]')
    # print('return:', return_div.text)
    
    # date_div = card.find_element(by='xpath', value='(.//div[@class="chakra-stack css-y25wms"])[2]')
    # print('date:', date_div.text)
    
    # valuation_div = card.find_element(by='xpath', value='(.//div[@class="chakra-stack css-y25wms"])[3]')
    # print('date:', valuation_div.text)
    
    df.append({
        'type': type_p,
        'n_doors': door_p,
        'status': status_span,
        'country': country_span,
        'title': title_h2,
        'price': price_p,
        'n_investor': investor_p,
        'n_detail': n_detail,
        'yield': return_div,
        'date_funded': date_div,
        'current_valuation': valuation_div,
        'total_rent_paid': paid_div,
        'other': other
        })


    print("=" * 40)
    
    
    
df = pd.DataFrame(df)

#%%

df['location'] = df['title'].apply(lambda x: (x.split(' in ')[1].strip()) if (len(x.split(' in ')) > 0) else x)
df 

#%%

df.to_csv('scraping_getstake/result.csv', index=False)

#%% TESTING SCROLL

height = web.execute_script("return document.querySelector('.infinite-scroll-component__outerdiv').scrollHeight ")
web.execute_script("document.querySelector('.infinite-scroll-component__outerdiv').scrollTo(0, document.querySelector('.infinite-scroll-component__outerdiv').scrollHeight )")
time.sleep(10)
height_new = web.execute_script("return document.querySelector('.infinite-scroll-component__outerdiv').scrollHeight ")
print('Height before:', height)
print('Height after:', height_new)


#%%

sold_button = web.find_element(by='xpath', value='//button[@href="/home/properties?status=sold"]')
sold_button.click()

actions = ActionChains(web)

# Scroll down using the PAGE_DOWN key
actions.send_keys(Keys.PAGE_DOWN).perform()

# You can repeat this or combine with other keys to scroll more
# Example to scroll to the bottom of the page:
actions.send_keys(Keys.END).perform()

#%%
card_divs = web.find_elements(by='xpath', value='//div[@class="css-zjen6v"]')
len(card_divs)







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


s = Service("./geckodriver")
o = Options()
o.add_argument("-profile")
o.add_argument("/home/saidahmad/snap/firefox/common/.mozilla/firefox/0omewp0q.myscraper")
o.headless = True

web = webdriver.Firefox(service=s, options=o)

time.sleep(2)

df = pd.DataFrame()

for i in range(1, 5):
    
    web.get(f"https://www.channele2e.com/mergers-and-acquisitions-2019?page={i}")
    
    
    time.sleep(3)
    try:
        table = web.find_element(By.XPATH, '//table')
        print("There is table")
    except ElementNotInteractableException:
        print("Can't click!")
    except TimeoutException:
        print("Can't find!")
    
    tr = table.find_element(By.XPATH, '//tr')
    ths = tr.find_elements(By.XPATH, '//th')
    cols = []
    for th in ths:
        cols.append(th.text)
    print(cols)
    print(len(cols))
    
    dftemp = []
    
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    trs = tbody.find_elements(By.TAG_NAME, 'tr')
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        temp = {}
        for i, td in enumerate(tds):
            temp[cols[i]] = td.text
        dftemp.append(temp)
    dftemp = pd.DataFrame(dftemp)
    
    df = pd.concat([df, dftemp])
    
    time.sleep(2)
#%%



# moth = web.find_element(By.XPATH, '//*[@id="locations"]')
# elems = web.find_elements(By.XPATH, '//li')
# for elem in elems:
#     mailelem = elem.find_element(By.XPATH, '//a[@class="spr-icon spr-email oda-tracked"]')
#     test = mailelem.get_attribute('href')
#     print(test)

time.sleep(3)

web.quit()
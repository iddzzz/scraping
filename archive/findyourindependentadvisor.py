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

web = webdriver.Firefox(service=s, options=o)

time.sleep(3)

web.get("https://www.findyourindependentadvisor.com/FindAdvisor?zipCode=90001")


time.sleep(3)
try:
    web.find_element(By.XPATH, '//*[@id="agree-to-terms"]').click()
    print("Clicked!")
except ElementNotInteractableException:
    print("Can't click!")
except TimeoutException:
    print(f"Can't find!")
time.sleep(5)

moth = web.find_element(By.XPATH, '//*[@id="locations"]')
elems = web.find_elements(By.XPATH, '//li')
for elem in elems:
    mailelem = elem.find_element(By.XPATH, '//a[@class="spr-icon spr-email oda-tracked"]')
    test = mailelem.get_attribute('href')
    print(test)

time.sleep(3)

web.quit()
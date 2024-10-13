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

web.get("https://www.upwork.com")

#%%

time.sleep(3)

web.quit()
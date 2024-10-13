import requests
from bs4 import BeautifulSoup
import time
import numpy as np

url = 'https://apps.apple.com/us/genre/ios-food-drink/id6023'
params = {'letter': 'A', 'page': 2}
r = requests.get(url, params=params)

time.sleep(5)

soup = BeautifulSoup(r.content, "html.parser")
soup = soup.find('table')
print(soup.text)

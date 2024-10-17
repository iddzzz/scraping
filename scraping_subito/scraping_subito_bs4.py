#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 09:25:20 2024

@author: saidahmad
"""

import numpy as np
import pandas as pd 
import requests
import time 
from bs4 import BeautifulSoup

#%% SCRAPE 1 PAGE

# URL to scrape
url = 'https://www.subito.it/annunci-italia/affitto/appartamenti/?o=1'

# Send a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <div> elements with the class "items__item"
    items = soup.find_all('div', class_='items__item')
    
    # Loop through the found items
    df = []
    for item in items:
        title_h2 = item.find('h2')
        if title_h2:
            print("title:", title_h2.get_text(strip=True))
            df.append({'title': title_h2.get_text(strip=True)})
        
            loc_date = item.find('div', class_="PostingTimeAndPlace-module_date-location__1Owcv index-module_container__noDE3")
            if loc_date:
                city = loc_date.find('span', class_="index-module_town__2H3jy")
                print("city:", city.get_text(strip=True))
                df[-1]["city"] = city.get_text(strip=True)
                
                city_code = loc_date.find('span', class_="city")
                print("city code:", city_code.get_text(strip=True))
                df[-1]["city_code"] = city_code.get_text(strip=True)
                
                loc_date_span = loc_date.find_all('span')
                try:
                    date = loc_date_span[2]
                    print("date:", date.get_text(strip=True))
                    date = date.get_text(strip=True)
                except:
                    date = np.nan
                df[-1]["date"] = date
            
            price_p = title_h2.next_sibling.next_sibling
            if price_p:
                print(price_p.get_text(strip=True))
                df[-1]["price"] = price_p.get_text(strip=True)
                
            other_div = price_p.next_sibling
            if other_div:
                other_p = other_div.find_all('p')
                area = np.nan
                nroom = np.nan 
                floor = np.nan 
                ntoilet = np.nan 
                nother = np.nan 
                for p in other_p:
                    text = p.get_text(strip=True)
                    if 'mq' in text: 
                        area = text
                    elif 'Local' in text:
                        nroom = text 
                    elif 'Pian' in text:
                        floor = text 
                    elif 'Bagn' in text:
                        ntoilet = text
                    else:
                        nother = text
                print("area:", area)
                print("n room:", nroom)
                print("floor:", floor)
                print("n toilet:", ntoilet)
                print("other:", nother)
                df[-1]["area"] = area 
                df[-1]["n_room"] = nroom 
                df[-1]["floor"] = floor 
                df[-1]["n_toilet"] = ntoilet 
                df[-1]["other"] = nother 
                        
        print("=" * 40)
        
    df = pd.DataFrame(df)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


#%% SCRAPE MANY PAGES 

dftotal = pd.DataFrame()

for i in range(10):
    time.sleep(np.abs(np.random.uniform(5, 15)))

    # URL to scrape
    url = f'https://www.subito.it/annunci-italia/affitto/appartamenti/?o={i}'
    
    # Send a request to the website
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        break
        
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <div> elements with the class "items__item"
    items = soup.find_all('div', class_='items__item')
    
    # Loop through the found items
    df = []
    for item in items:
        title_h2 = item.find('h2')
        if title_h2:
            print("title:", title_h2.get_text(strip=True))
            df.append({'title': title_h2.get_text(strip=True)})
        
            loc_date = item.find('div', class_="PostingTimeAndPlace-module_date-location__1Owcv index-module_container__noDE3")
            if loc_date:
                city = loc_date.find('span', class_="index-module_town__2H3jy")
                print("city:", city.get_text(strip=True))
                df[-1]["city"] = city.get_text(strip=True)
                
                city_code = loc_date.find('span', class_="city")
                print("city code:", city_code.get_text(strip=True))
                df[-1]["city_code"] = city_code.get_text(strip=True)
                
                loc_date_span = loc_date.find_all('span')
                try:
                    date = loc_date_span[2]
                    print("date:", date.get_text(strip=True))
                    date = date.get_text(strip=True)
                except:
                    date = np.nan
                df[-1]["date"] = date
            
            price_p = title_h2.next_sibling.next_sibling
            if price_p:
                print(price_p.get_text(strip=True))
                df[-1]["price"] = price_p.get_text(strip=True)
                
            other_div = price_p.next_sibling
            if other_div:
                other_p = other_div.find_all('p')
                area = np.nan
                nroom = np.nan 
                floor = np.nan 
                ntoilet = np.nan 
                nother = np.nan 
                for p in other_p:
                    text = p.get_text(strip=True)
                    if 'mq' in text: 
                        area = text
                    elif 'Local' in text:
                        nroom = text 
                    elif 'Pian' in text:
                        floor = text 
                    elif 'Bagn' in text:
                        ntoilet = text
                    else:
                        nother = text
                print("area:", area)
                print("n room:", nroom)
                print("floor:", floor)
                print("n toilet:", ntoilet)
                print("other:", nother)
                df[-1]["area"] = area 
                df[-1]["n_room"] = nroom 
                df[-1]["floor"] = floor 
                df[-1]["n_toilet"] = ntoilet 
                df[-1]["other"] = nother 
                        
        print("=" * 40)
        
    df = pd.DataFrame(df)
    dftotal = pd.concat([dftotal, df])
    dftotal = dftotal.drop_duplicates().reset_index(drop=True)


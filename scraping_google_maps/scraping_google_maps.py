#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 07:23:06 2024

@author: saidahmad
"""

import numpy as np 
import pandas as pd 
import time 
import psutil 
import os 
import sys
import itertools
import string
import sqlite3
from seleniumbase import Driver 

import google.auth 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.append("../personaldata")
sys.path.append("personaldata")
import personaldata

from personaldata import SAMPLE_SPREADSHEET_ID


#%% SPREADSHEET AUTHENTICATION

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.

SAMPLE_RANGE_NAME = "Sheet1!A1:D1"

CREDENTIAL = "credentials/google-spreadsheet-credentials.json"
TOKEN = "credentials/token.json"

def authenticate():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIAL, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN, "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("sheets", "v4", credentials=creds)
      
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])
      
        if not values:
            print("No data found.")
            return
      
        for row in values:
            print(len(row))
            for cell in row:
                print(cell)
    except HttpError as err:
        print(err)

# authenticate()

#%% SPREADSHEET FUNCTION

def append_values(token, scope, spreadsheet_id, range_name, value_input_option, values):

    creds = Credentials.from_authorized_user_file(token, scope)
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

# append_values(
#       TOKEN, SCOPES,
#       SAMPLE_SPREADSHEET_ID,
#       "Sheet1",
#       "USER_ENTERED",   
#       [["nama", "alamat", "web", "no hp", "url"]],
#   )


#%%


dfproxy = pd.read_csv("proxy/proxyList.txt")
proxy = dfproxy["proxy"].sample(1).values[0]
proxy = proxy.replace("http://", "")

web = Driver(uc=True, user_data_dir=personaldata.chrome_profile_bumblebee,
             proxy=proxy
             # chromium_arg="--no-proxy-server,--disable-extensions"
             )
web.uc_open_with_reconnect("https://www.instagram.com/", 4)
time.sleep(5) 
web.get("https://www.google.com/maps/")


#%% SEARCH

city = "Paris"
entity = "Law Firm"

search_input = web.find_element(by='xpath', value='//*[@id="searchboxinput"]')
search_input.clear()
search_input.send_keys(city) 

time.sleep(2)

search_button = web.find_element(by='xpath', value='//*[@id="searchbox-searchbutton"]')
search_button.click()

time.sleep(5)

search_input = web.find_element(by='xpath', value='//*[@id="searchboxinput"]')
search_input.clear()
search_input.send_keys(entity)

time.sleep(2) 

search_button = web.find_element(by='xpath', value='//*[@id="searchbox-searchbutton"]')
search_button.click()

time.sleep(5)

#%% SCROLL TILL THE END

iattempt = 0
nattempt = 5

i = 0 
n = 3

while True:
    feed_div = web.find_element(by='xpath', value='//div[@role="feed"]')
    
    height = web.execute_script("return arguments[0].scrollHeight", feed_div)
    # print('height:', height)
    
    web.execute_script("""
        arguments[0].scrollTo({
            top: arguments[0].scrollHeight,
            left: 0,
            behavior: 'smooth'
        });
    """, feed_div)
    
    time.sleep(np.random.uniform(2, 10))
    
    height_new = web.execute_script("return arguments[0].scrollHeight", feed_div)
    # print('height new:', height_new)
    
    if height_new == height:
        iattempt += 1 
        print("Attempt", iattempt)
        if iattempt >= nattempt:
            print("Maximum number of attempts achieved.")
            break
        continue
    
    iattempt = 0 
    
    i += 1
    if i >= n:
        break

#%% SCRAPE CARDS

dfurl = []

feed_div = web.find_element(by='xpath', value='//div[@role="feed"]') 
card_divs = feed_div.find_elements(by='xpath', value='./div')
j = 1
for i in range(len(card_divs)):
    cards = feed_div.find_elements(by='xpath', value='./div')
    link_as = cards[i].find_elements(by='xpath', value='.//a')
    if not bool(len(link_as)): continue
    print(j, link_as[0].get_attribute("aria-label"))
    if link_as[0].get_attribute("aria-label") is None: continue
    dfurl.append({
        'name': link_as[0].get_attribute("aria-label"),
        'url': link_as[0].get_attribute("href")
        })
    j += 1

dfurl = pd.DataFrame(dfurl)


#%% SCRAPE DETAILS


for i, row in dfurl.iterrows():
    web.get(row["url"])
    
    time.sleep(np.random.uniform(5, 8))
    
    # print(row["name"])
    
    address = web.find_elements(by='xpath', value='//*[@data-item-id="address"]')
    address = address[0].get_attribute("aria-label") if bool(len(address)) else ""
    # print(address)
    
    website = web.find_elements(by='xpath', value='//*[@data-item-id="authority"]')
    website = website[0].get_attribute("aria-label") if bool(len(website)) else ""
    # print(website)
    
    phone = web.find_elements(by='xpath', value='//*[@data-tooltip="Copy phone number"]')
    phone = phone[0].get_attribute("aria-label") if bool(len(phone)) else ""
    # print(phone)
    
    # print(row["url"])
    
    append_values(
          TOKEN, SCOPES,
          SAMPLE_SPREADSHEET_ID,
          "Sheet1",
          "USER_ENTERED",   
          [[row["name"], address, website, phone, row["url"]]],
      )
    
    # print("=" * 40)
    
    time.sleep(np.random.uniform(2, 7))


#%%

web.close()
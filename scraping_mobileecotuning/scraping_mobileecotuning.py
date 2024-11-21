#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:32:46 2024

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
import re
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

#%%

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_RANGE_NAME = "Sheet1!A1:D1"

CREDENTIAL = "credentials/google-spreadsheet-credentials.json"
TOKEN = "credentials/token.json"

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
             proxy=proxy,
             # chromium_arg="--no-proxy-server,--disable-extensions"
             )
web.uc_open_with_reconnect("https://mobileecotuning.com/find-an-agent/", 4)

#%%

iframe = web.find_element('xpath', '//iframe[@id="bensky_map"]') 
web.switch_to.frame(iframe)


dealermap_div = web.find_element('xpath', '//div[@id="dealermap"]')

#%%

web.get("https://portal.mobileecotuning.com/dealer-map.php?")

#%%

div_parent = web.find_element(by='xpath', value='//*[@id="dealermap"]/div/div[3]/div[1]/div[2]/div/div[3]')

divs = div_parent.find_elements(by='xpath', value='./div')
for div in divs:
    print(div.get_attribute("title"))
    title = div.get_attribute("title")
    if title == "":
        continue
    div.click()
    
    time.sleep(3)
    
    card = web.find_element(by='xpath', value='//div[@class="infowindow text-dark"]')
    text = card.text
    
    
    search = re.search("Type[\w\:\ ]*", text)
    if search is not None:
        print(search.group(0))
        mytype = search.group(0)
    else:
        mytype = ""
    
    search = re.search("\+\d+", text)
    if search is not None:
        print(search.group(0))
        phone = search.group(0)
    else:
        phone = ""
    
    search = re.search("\w+\@[\w\.]+", text)
    if search is not None:
        print(search.group(0))
        email = search.group(0)
    else:
        email = ""
    
    search = re.search("http[\:\w\.\-\/]*", text)
    if search is not None:
        print(search.group(0))
        website = search.group(0)
    else:
        website = ""
    
    
    append_values(
          TOKEN, SCOPES,
          SAMPLE_SPREADSHEET_ID,
          "Sheet2",
          "USER_ENTERED",   
          [["Manchester", title, mytype, phone, email, website]],
      )
    
    
    web.find_element(by='xpath', value='//button[@aria-label="Close"]').click()
    time.sleep(3)
    
    


#%%

search = re.search("Type[\w\:\ ]*", text)
if search is not None:
    print(search.group(0))

search = re.search("\+\d+", text)
if search is not None:
    print(search.group(0))

search = re.search("\w+\@[\w\.]+", text)
if search is not None:
    print(search.group(0))

#%%

web.close()
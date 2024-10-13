#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 07:32:30 2024

@author: saidahmad
"""

import requests
from bs4 import BeautifulSoup

# URL for the Amazon product search page
url = 'https://www.amazon.com/s?k=cooker&page=1'

# Set up headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Make the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product <div> elements with attribute data-component-type="s-search-result"
    product_divs = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Loop through each product div and get the title from <h2>
    for product in product_divs:
        title = product.find('h2')
        if title:
            product_title = title.get_text(strip=True)
            print(product_title)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
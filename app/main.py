#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

URL = "https://coinmarketcap.com/all/views/all/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='cmc-table-row')
    valuts = []
    for item in items:
        valuts.append({
            #'title': item.find('a'),
            'name': item.find('a', class_='cmc-link').get_text(strip=True),
            'price':item.find('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price').get_text(strip=True),
            # 'hour':,
            # 'day':,
            # "week":,
        })
    print(valuts)

def parse():
    html=get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Error")

parse()
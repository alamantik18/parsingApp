#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import json

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
            'title': item.find('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__symbol').get_text(strip=True),
            'name': item.find('a', class_='cmc-link').get_text(strip=True),
            'price':item.find('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price').get_text(strip=True),
            'hour':item.find('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h').get_text(),
            'day':item.find('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h').get_text(),
            'week':item.find('td', class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-7-d').get_text(),
        })
    return valuts

def save_file(items, path):
    to_json = {'coins': items}
    with open(path, 'w', newline='') as file:
        json.dump(to_json, file, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=4, separators=None, default=None, sort_keys=False)
    with open(path) as file:
        print(file.read())    

def parse():
    html=get_html(URL)
    if html.status_code == 200:
        valuts = get_content(html.text)
        save_file(valuts, 'valuts.json')
    else:
        print("Error")

parse()
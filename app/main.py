#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import json

URL = "https://coinmarketcap.com/all/views/all/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='cmc-table__table-wrapper-outer')[2]
    trs = items.find_all('tr')[1:]
    valuts = {}
    for tr in trs:
        tds = tr.find_all('td')

        name = tds[1].text
        symbol = tds[2].text
        price = (tds[4].text).replace('$', '').replace(',', '')
        hour = tds[7].text
        day = tds[8].text
        week = tds[9].text

        valuts.update({symbol: {
                       'name': name,
                       'price': price,
                       'hour': hour,
                       'day': day,
                       'week': week}})
    return valuts


def save_json(data, path):
    if data:
        with open(path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)   

def parse():
    html=get_html(URL)
    if html.status_code == 200:
        valuts = get_content(html.text)
        save_json({'coins': valuts}, 'valuts.json')
    else:
        print("Error")

if __name__ == "__main__":
    parse()
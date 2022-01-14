import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://coinmarketcap.com/'
HEADERS = {'user-agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
           'accept': '*/*'}
FILE = 'currencies.csv'
COUNT_MAX = 25

def get_html(url, params=None): # get content
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("tr", class_='cmc-table-row')
    currencies = []
    count = 0
    for item in items:
        currencies.append({
            'name': item.find('div', class_='cmc-table__column-name sc-1kxikfi-0 eTVhdN').get_text(), #strip=True
            'market_cap': item.find('td', class_='cmc-table__cell ' +
                                    'cmc-table__cell--sortable cmc-table__cell--right ' +
                                    'cmc-table__cell--sort-by__market-cap').get_text(),
            'price': item.find('td', class_='cmc-table__cell cmc-table__cell--sortable ' +
                               'cmc-table__cell--right cmc-table__cell--sort-by__price').get_text(),
        })
        count += 1
        if count == COUNT_MAX:
            break
    #print(currencies)
    #print(len(currencies))
    return currencies

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'market cap', 'price'])
        for item in items:
            writer.writerow([item['name'], item['market_cap'], item['price']])

def search_info(items):
    count = 0
    while 1:
        name = input('\nEnter name of cripto, or for exit enter q:\n')
        if name == 'q':
            return
        for item in items:
            if item.get('name') == name:
                print("market capitalization:", item.get('market_cap'))
                print("cost 1 v. in USA$:", item.get('price'))
                break
            count += 1
            if count == COUNT_MAX:
                print("Not found!\n")
                count = 0
            
    
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        currencies = get_content(html.text)
        save_file(currencies, FILE)
        print("Parse is done")
        search_info(currencies)
    else:
        print('Error')

parse()

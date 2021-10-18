import requests

import random

import time

from bs4 import BeautifulSoup

import re

import csv


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#URL = 'http://www.catalogfactory.org/okved2/06.1'

def get_html(url, params = None):
    req = requests.get(url, headers = HEADERS, params = params)
    return req

def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_= '')

    links = []

    for item in items:
        links.append(item.get('href'))

    return links[:-5]

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('p', class_ = '')

    info = []
    
    for item in items:

        address = re.findall(r'адрес:.*\)', str(item))
        inn = re.findall(r'инн:\s\d*', str(item).lower())

        info.append({
            'name' : item.find('a', class_ = '').get_text(),
            'address' : address[0][6:len(address[0])-1],
            'inn' : inn[0][4:]
        })

    return info
        
def get_pages_count(html, link):
    soup = BeautifulSoup(html, 'html.parser')

    pages = soup.select(f'a[href^="{link}"]')

    pages = len(pages) - 2

    return pages

def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:

        links = get_links(html.text)
        
        for link in links:

            url = 'http://www.catalogfactory.org' + link

            html = get_html(url)

            info = []

            page_count = get_pages_count(html.text, link)
            
            print(url)

            for page in range(1, page_count + 1):
                print(f'Парсинг {page} из {page_count}...')
                html = get_html(url + f'/{page}')
                get_content(html.text)

                time.sleep(random.randint(1, 2))

                info.extend(get_content(html.text))

            field_names = ['name', 'address', 'inn']

            with open(link.replace("/", '_') + '.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = field_names, quotechar = ';')
                writer.writeheader()
                writer.writerows(info)

            time.sleep(random.randint(7, 15))

    else:
        print('Error')

parse('http://www.catalogfactory.org/okved2.html?okved=06')
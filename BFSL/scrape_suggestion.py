
import requests
import pickle
import os
import pandas as pd

from bs4 import BeautifulSoup
from collections import defaultdict
from time import sleep
from time import time
from math import exp


from BFSL.statussaver import _update_statusdict
from BFSL.statussaver import _store_statusdict, _load_statusdict

try:
    STATUSDICT = defaultdict(lambda : None, _load_statusdict('STATUSDATA.pickle'))
except:
    from BFSL.statussaver import STATUSDICT


BASE = 'https://www.borgerforslag.dk/se-og-stoet-forslag/?Id=FT-'


def page_call(five_digit_number):
    ''' Return the request of a page
    '''
    UA = {'User-Agent': 'For research and/or education'}
    response = requests.get(BASE + five_digit_number, headers = UA)

    if response.status_code == 200:
        _update_statusdict(five_digit_number, True)
        _store_statusdict(STATUSDICT)
        print('Storing page {} as good hit'.format(five_digit_number))
        return response

    else:
        _update_statusdict(five_digit_number, False)
        _store_statusdict(STATUSDICT)
        print('Storing page {} as miss'.format(five_digit_number))
        return None





def format_page(page_response):
    ''' Converts the html to a row of data
    '''
    soup = BeautifulSoup(page_response.text, 'html.parser')
    article = soup.find_all('div', attrs = {'class':'article'})[0]

    row = {}

    title = article.find_all('span', attrs = {'data-reactid':'5'})[0].text
    subtitle = article.find_all('span', attrs = {'data-reactid':'44'})[0].text
    text = article.find_all('div', attrs = {'class':'public-DraftEditor-content'})[1].text

    start_date = article.find_all('strong', attrs = {'data-reactid':'11'})[0].text
    end_date = article.find_all('strong', attrs = {'data-reactid':'14'})[0].text
    supporters = article.find_all('strong', attrs = {'data-reactid':'17'})[0].text

    row['title'] = title
    row['subtitle'] = subtitle
    row['start_date'] = start_date
    row['end_date'] = end_date
    row['supporters'] = supporters
    row['text'] = text

    return row



def scrape(list_of_pages, save = True):
    ''' Does the actual scraping
    '''
    final = pd.DataFrame({'title':[],
                          'subtitle':[],
                          'start_date':[],
                          'end_date':[],
                          'supporters':[],
                          'text':[]})

    for page in list_of_pages:
        print('Beginning page {}'.format(page))

        sleep(10)

        if STATUSDICT[page] == False:
            continue

        t0 = time()

        page_return = page_call(page)

        if page_return is None:
            print('Page {} was added as miss in the statusdict'.format(page))
            continue

        formatted_row = format_page(page_return)

        t1 = time()
        sleep((t1-t0))

        final = final.append(formatted_row, ignore_index = True)

    if save:
        final.to_csv('BFSL.csv')

    return final




def list_from_integers(first, last):
    ''' formats a range of integers for retrieving
    '''
    return [str(i).zfill(5) for i in range(first, last)]




scrapelist = list_from_integers(5, 852)
scrape(scrapelist)

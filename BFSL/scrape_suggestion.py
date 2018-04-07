
import requests
import pickle
import os
import pandas as pd

from bs4 import BeautifulSoup
from collections import defaultdict
from time import sleep
from time import time
from math import exp

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
        #_update_statusdict(five_digit_number, True)
        STATUSDICT[five_digit_number] = True
        _store_statusdict(STATUSDICT)
        print('Storing page {} as good hit'.format(five_digit_number))
        return response

    else:
        STATUSDICT[five_digit_number] = False
#        _update_statusdict(five_digit_number, False)
        _store_statusdict(STATUSDICT)
        print('Storing page {} as miss'.format(five_digit_number))
        return None





def format_page(page_response, page):
    ''' Converts the html to a row of data
    '''
    soup = BeautifulSoup(page_response.text, 'html.parser')
    article = soup.find_all('div', attrs = {'class':'article'})[0]

    row = {}
    # ~~~~ TITLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    title = article.find_all('span', attrs = {'data-reactid':'5'})[0].text
    # ~~~~ SUBTITLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    try:
        subtitle = article.find_all('span', attrs = {'data-reactid':'44'})[0].text
    except:
            subtitle = article.find_all('span', attrs = {'data-reactid':'49'})[0].text
    # ~~~~ TEXT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    try:
        text = article.find_all('div', attrs = {'class':'public-DraftEditor-content'})[1].text
    except:
            text = article.find_all('div', attrs = {'class':'public-DraftEditor-content'})[2].text
    # ~~~~ START/END DATE & SUPPORTERS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    try:
        start_date = article.find_all('strong', attrs = {'data-reactid':'11'})[0].text
        end_date = article.find_all('strong', attrs = {'data-reactid':'14'})[0].text
        supporters = article.find_all('strong', attrs = {'data-reactid':'17'})[0].text

    except:
        start_date = article.find_all('strong', attrs = {'data-reactid':'14'})[0].text
        end_date = article.find_all('strong', attrs = {'data-reactid':'17'})[0].text
        supporters = article.find_all('strong', attrs = {'data-reactid':'20'})[0].text

    row['title'] = title
    row['subtitle'] = subtitle
    row['start_date'] = start_date
    row['end_date'] = end_date
    row['supporters'] = supporters
    row['text'] = text
    row['page'] = page

    return row



def scrape(list_of_pages):
    ''' Does the actual scraping
    '''
    final = pd.DataFrame({'title':[],
                          'subtitle':[],
                          'start_date':[],
                          'end_date':[],
                          'supporters':[],
                          'text':[]})

    for page in list_of_pages:
        # this try except ensures that we dont loose data if something fails
        try:

            if STATUSDICT[page] == False:
                continue

            print('Beginning page {}'.format(page))
            sleep(10)
            t0 = time()

            page_return = page_call(page)

            if page_return is None:
                continue

            formatted_row = format_page(page_return, page)
            t1 = time()
            sleep((t1-t0))

            final = final.append(formatted_row, ignore_index = True)

        except:
            print('Encountered issue at page {} - continuing'.format(page))
            continue

    return final



def save_csv(dataframe):
    ''' Saves and/or appends to the data, depending on whether it exists or not
    '''
    print('saving file')
    if not os.path.exists('BFSL.csv'):
        dataframe.to_csv('BFSL.csv')
    else:
        dataframe.to_csv('BFSL.csv', mode = 'a', header = False)




def list_from_integers(first, last, thinlist = True):
    ''' formats a range of integers for retrieving
    '''
    all_ints = [str(i).zfill(5) for i in range(first, last)]

    if thinlist:
        if os.path.exists('BFSL.csv'):
            data = pd.read_csv('BFSL.csv')
            all_ints = [i for i in all_ints if int(i) not in list(data['page'])]

    return all_ints


def MAIN(save = True):
    scrapelist = list_from_integers(5, 855)
    data = scrape(scrapelist)

    if save:
        save_csv(data)

    print('DONE')

MAIN()

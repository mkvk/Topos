#!/usr/bin/env python3

"""
This Python code is used to scrape the wiki website of most populous cities and
add extra information from each other wiki webpages of most populous cities.

Requisites : This project requires python 3 environment with "requests" "BeautifulSoup4" and "pandas" libraries pre-installed. 
If not, they maybe be installed via "pip install requests BeautifulSoup4 pandas".

Author : Murali Kammili
"""

# import necessary libraries
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import pandas as pd

# Helper functions and Error logging
def simple_get(url):
    """
    Fetch the content of URL by making an HTTP GET request.
    If the content type of response is some kind of HTML/XML,
    return the text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML,
    otherwise return False.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    Print the error.
    """
    print(e)


if __name__ == "__main__" :

    # get the wiki url of most popular cities in US ranked by population
    raw_html = simple_get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
    html = BeautifulSoup(raw_html, 'html.parser')

    # the below dictionary structure represents the column names of table in which we are going to store after scraping
    table_data = {'_2018_Rank' : [] ,
            'City' : [] ,
            'State' : [] ,
            '_2018_Estimate' : [] ,
            '_2010_Census' : [] ,
            'Change' : [] ,
            '_2016_land_area_mi' : [] ,
            '_2016_land_area_km' : [] ,
            '_2016_population_density_mi': [],
            '_2016_population_density_km' : [] ,
            'Location' : [] ,
            'Official_Website' : [] # This field is added beyond the main table on wiki page url
            }

    # Locate the table element and fetch the desired table class from the page
    table = html.find('table',{'class':'wikitable sortable'})
    # Find all the table data tags and store them
    tds = table.findAll('td')

    i=1 # variable to fill the respective columns of table from top to bottom and left to right
    # loop to mimic switch case to fill the values of respective keys in "table_data" dictionary
    for td in tds :
        if i%11 == 1 :
            table_data['_2018_Rank'].append(td.text.strip())
        elif i%11 == 2 :
            # regular expression substitution to clean the data
            cl = re.sub(r"\[[A-Za-z0-9]+\]", "", td.text.strip())
            table_data['City'].append(cl)
        elif i%11 == 3 :
            cl = re.sub(r"\[[A-Za-z0-9]+\]", "", td.text.strip())
            table_data['State'].append(cl)
        elif i%11 == 4 :
            table_data['_2018_Estimate'].append(td.text.strip())
        elif i%11 == 5 :
            table_data['_2010_Census'].append(td.text.strip())
        elif i%11 == 6 :
            table_data['Change'].append(td.text.strip())
        elif i%11 == 7 :
            table_data['_2016_land_area_mi'].append(td.text.strip())
        elif i%11 == 8 :
            table_data['_2016_land_area_km'].append(td.text.strip())
        elif i%11 == 9 :
            table_data['_2016_population_density_mi'].append(td.text.strip())
        elif i%11 == 10 :
            table_data['_2016_population_density_km'].append(td.text.strip())
        elif i%11 == 0 :
            cl = td.text.strip()
            # regular expression substitution to obtain the desired data
            cl = re.sub(r"\xa0", "", cl)
            cl = re.sub(r"\ufeff", "", cl)
            cl = re.sub(r" / ", "", cl)
            cl = re.sub(r"\d+\W\d+\W\d+\W[A-Z] \d+\W\d+\W\d+\W[A-Z]", "", cl)
            cl = re.sub(r"\d+.\d+;.*$", "", cl)
            table_data['Location'].append(cl)

            # for each city fetch it's webpage link by finding the html anchor tag
            tr = table.findAll('tr')[(int)(i/11)]
            web = tr.findAll('a')[0]
            web = web.get('href')
            # since the obtained link is partial, supplement by appending to form complete link
            web = 'https://en.wikipedia.org'+web

            # Now fetch the respective webpage of a city
            # and scrape it to find the official website link present in one of the tables
            c_raw_html = simple_get(web)
            c_html = BeautifulSoup(c_raw_html, 'html.parser')
            wiki_table = c_html.find('table', {'class': 'infobox geography vcard'})

            # after locating the table of interest, fetch all rows and reverse the list
            # (since the official website link is observed to be present more near to the bottom of table)
            trs = wiki_table.findAll('tr')
            trs.reverse()
            for tr in trs :
                ths = tr.findAll('th')
                for th in ths :
                    # among all the table headings, find the one which has "Website" text
                    if th.text=="Website" :
                        # fetch the link and add to the dictionary
                        a = tr.findAll('a')[0]
                        a=a.get('href')
                        table_data['Official_Website'].append(a)
                        break

        i+=1

    # load the disctinary to pandas dataframe
    df = pd.DataFrame(table_data)
    # print the contents of data frame if required
    #print(df)
    # the below line saves the data to a CSV file at given path locally
    #df.to_csv("C:/.../Wiki_Cities_data.csv" , index=False , encoding='utf-8')

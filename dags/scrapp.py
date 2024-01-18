# from bs4 import BeautifulSoup
# import requests
# import re, sys, argparse
# import pandas as pd
# import datetime
# from datetime import timedelta
# from dateutil import parser
# from selenium.webdriver.chrome.service import Service 
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# def all_news_link(url):
#     r  = requests.get(url)
#     data = r.text
#     soup = BeautifulSoup(data, features="lxml")
#     all_link=set()
#     for link in soup.find_all('a'):
#         if(link.get('href')!=None):
#             if(re.search(r'\bread\b', link.get('href'))!=None) and len(re.findall(r'koran.bisnis',link.get('href'))) == 0:
#                 all_link.add(link.get('href'))
#     return all_link

# def get_data(url):
#     chrome_options = Options()
#     chrome_options.add_argument("--headless=new") 
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument('--allow-running-insecure-content')
#     chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     chrome_options.add_argument('--ignore-certificate-errors')
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     driver.get(url)
#     soup3 = BeautifulSoup(driver.page_source, 'html.parser')

#     try:
#         try :
#             title = soup3.find('div', {'class':'container kanal_container'}).find_all('h1', {'class' : 'title-only'})[0].text
#         except :
#             title = soup3.find('div', {'class':'col-custom left'}).find('h1').text
#         content = soup3.find('div', {'class':'row sticky-wrapper'}).find('div', {'class': 'col-sm-10'}).find_all('p')
#         content = ' '.join([content[i].text for i in range(0, len(content))]).replace('Simak berita lainnya seputar topik artikel ini, di sini :', '').strip()
#     except Exception as e:
#         print('failed to get data', url, e)
#         title = ''
#         content = ''

#     driver.quit()
#     return title, content

# def get_data_from_url(url):
#     c = 0
#     link_news = []
#     jsonlist = []
#     while c == 0 or len(link_news) > 0 :
#         c += 1
#         uri = url+str(c)
#         link_news = all_news_link(uri)
#         print('start read from : %s'%uri)
#         for i in link_news:
#             temp = {}
#             temp['title'], temp['content'] = get_data(i)
#             temp['url'] = i
#             if temp['title'] and temp['content'] : jsonlist.append(temp)
#     return jsonlist

# def generate_date(date):
#     dict_month = {
#         1 : 'January',
#         2 : 'February',
#         3 : 'March',
#         4 : 'April',
#         5 : 'May',
#         6 : 'June',
#         7 : 'July',
#         8 : 'August',
#         9 : 'September',
#         10 : 'Oktober',
#         11 : 'November',
#         12 : 'December'
#     }
#     day = str(date.day)
#     month = dict_month[date.month]
#     if len(day) < 2 :
#         day = '0'+day
#     year = date.year
#     return day, month, year

# def generate_url_by_date(sd, ed, channel):
#     #https://www.bisnis.com/index/page/?c=43&d=01%20April%202020&d=01+April+2020&per_page=
#     sd = parser.parse(sd)
#     ed = parser.parse(ed)
#     urls = {}
#     while sd <= ed :
#         day, month, year = generate_date(sd) 
#         url = 'https://www.bisnis.com/index/page/?c={}&d={}%20{}%20{}&d={}+{}+{}&per_page='.format(channel, day, month, year,day, month, year)
#         urls[sd] = url
#         sd += timedelta(days=1)
#     return urls

# if __name__ == "__main__":
#     parsers = argparse.ArgumentParser(description='example: python scraping_bisniscom.py -sd 2023-09-01 -ed 2023-09-20 -c 43')
#     parsers.add_argument('-sd', '--start_date', help='The Start Date - format YYYY-MM-DD', required=True, type=str)
#     parsers.add_argument('-ed', '--end_date', help='The Start Date - format YYYY-MM-DD', required=True, type=str)
#     parsers.add_argument('-c', '--channel', help='Channel category default 91 (Ekonomi % Business)', default=43, type=int)
#     args = parsers.parse_args()

#     start_date = str(args.start_date)
#     urls = generate_url_by_date(start_date, args.end_date, args.channel)
#     fo = '%s_%s_%d'%(str(args.start_date).replace('-', ''), str(args.end_date).replace('-',''), args.channel)+'.csv'
#     jsonlist = []
#     for date, url in urls.items():
#         jsonlist = jsonlist + get_data_from_url(url)
#         print(date, len(jsonlist))
#     df = pd.DataFrame(jsonlist)
#     df.to_csv(fo)
#     print('done, got %d save in %s'%(len(df), fo))

from bs4 import BeautifulSoup
import requests
import re, sys, argparse
import pandas as pd
import datetime
from datetime import timedelta
from dateutil import parser
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def all_news_link(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    all_link = set()
    for link in soup.find_all('a'):
        if(link.get('href') != None):
            if(re.search(r'\bread\b', link.get('href')) != None) and len(re.findall(r'koran.bisnis',link.get('href'))) == 0:
                all_link.add(link.get('href'))
    return all_link

def get_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
        title_element = driver.find_element(By.CSS_SELECTOR, ('h1>detailsTitleCaption'))
        title = title_element.text if title_element else ''

        content_elements = driver.find_elements(By.CSS_SELECTOR, ('article.detailsContent p'))
        content = ' '.join([elem.text for elem in content_elements]).replace('Simak berita lainnya seputar topik artikel ini, di sini :', '').strip()

        author_name_element = driver.find_element(By.CSS_SELECTOR, ('div.detailsAuthor'))
        author_name = author_name_element.text if author_name_element else ''
        
        details_attribute_dates_element = driver.find_element(By.CSS_SELECTOR, ('div.detailsAttributeDates'))
        details_attribute_dates = details_attribute_dates_element.text if details_attribute_dates_element else ''
        
    except Exception as e:
        print('failed to get data', url, e)
        title = ''
        content = ''
        author_name = ''
        details_attribute_dates = ''
    
    driver.quit()
    
    return title, content, author_name, details_attribute_dates

def get_data_from_url(url, max_retries=3):
    c = 0
    link_news = set()
    jsonlist = []
    retries = 0

    while retries < max_retries:
        c += 1
        uri = url + str(c)
        new_links = all_news_link(uri)
        print('start read from : %s' % uri)

        if not new_links:
            retries += 1
        else:
            retries = 0

        link_news.update(new_links)

        for i in link_news:
            temp = {}
            temp['title'], temp['content'], temp['author_name'], temp['details_attribute_dates'] = get_data(i)
            temp['url'] = i
            if temp['title'] and temp['content']:
                jsonlist.append(temp)

        if retries == max_retries:
            print("No new links found. Stopping the scraping.")
            break

    return jsonlist

def generate_date(date):
    dict_month = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'Oktober',
        11 : 'November',
        12 : 'December'
    }
    day = str(date.day)
    month = dict_month[date.month]
    if len(day) < 2:
        day = '0'+day
    year = date.year
    return day, month, year

def generate_url_by_date(sd, ed, channel):
    sd = parser.parse(sd)
    ed = parser.parse(ed)
    urls = {}
    while sd <= ed:
        day, month, year = generate_date(sd) 
        url = 'https://www.bisnis.com/index/page/?c={}&d={}%20{}%20{}&d={}+{}+{}&per_page='.format(channel, day, month, year,day, month, year)
        urls[sd] = url
        sd += timedelta(days=1)
    return urls

if __name__ == "__main__":
    parsers = argparse.ArgumentParser(description='example: python scraping_bisniscom.py -sd 2023-09-01 -ed 2023-09-20 -c 43')
    parsers.add_argument('-sd', '--start_date', help='The Start Date - format YYYY-MM-DD', required=True, type=str)
    parsers.add_argument('-ed', '--end_date', help='The Start Date - format YYYY-MM-DD', required=True, type=str)
    parsers.add_argument('-c', '--channel', help='Channel category default 43 (Ekonomi % Business)', default=43, type=int)
    args = parsers.parse_args()

    start_date = str(args.start_date)
    urls = generate_url_by_date(start_date, args.end_date, args.channel)
    fo = '%s_%s_%d'%(str(args.start_date).replace('-', ''), str(args.end_date).replace('-',''), args.channel)+'.csv'
    jsonlist = []
    for date, url in urls.items():
        jsonlist = jsonlist + get_data_from_url(url)
        print(date, len(jsonlist))
    df = pd.DataFrame(jsonlist)
    df.to_csv(fo, index=False)  # Set index=False to avoid writing row numbers as an extra column
    print('done, got %d save in %s'%(len(df), fo))

    #Error Message: no such element: Unable to locate element: {"method":"css selector","selector":"h1.detailsTitleCaption"} dst..


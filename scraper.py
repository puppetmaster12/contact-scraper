import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
from mail_spider import MailSpider

logging.getLogger('scrapy').propogate = False

def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)][:n]
    return urls

def ask_user(question):
    response = input(question + 'y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False

def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if response == False: return

    with open(path, 'wb') as file:
        file.close()

def get_info(tag, n, language, path, reject=[]):
    create_file(path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='w', header=True)

    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)

    print('Searching for emails...')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()

    print('Cleaning emails...')
    df = pd.read_csv(path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)

    return df

bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki']
df = get_info('tour companies in sri lanka', 5, 'pt', 'tour_emails.csv', reject=bad_words)
print(df.head())

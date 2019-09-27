import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
import MailSpider from mail_spider

logging.getLogger('scrapy').propogate = False

def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)][:n]
    return urls

result = get_urls('tour companies in sri lanka', 5, 'en')

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
        if response = False: return

    with open(path, 'wb') as file:
        file.close()

def get_info(tag, n, language, path, reject=[]):
    create_file(path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='w'. header=True)

    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)

    print('Searching for emails...')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls=google_urls)

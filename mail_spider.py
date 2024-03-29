import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search

class MailSpider(scrapy.Spider):
    name = 'email'

    def parse(self, response):
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):
        for word in self.reject:
            if word in str(response.url):
                return
        html_text = str(response.text)

        mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)

        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)

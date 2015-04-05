# -*- coding: utf-8 -*-
import re
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bs4 import BeautifulSoup as Soup
from jd.items import JdGoodsItem


class JdCategorySpider(CrawlSpider):
    name = "jd-category"
    allowed_domains = ["jd.com"]
    start_urls = (
        'http://www.jd.com/',
    )
    rules=(Rule(LinkExtractor(allow=('channel\.jd\.com/.*',))),
           Rule(LinkExtractor(allow=('item\.jd\.com/.*')),callback='parse_item'))
    

    def parse_item(self, response):
        s=Soup(response.body)
        items=s.find_all('a',href=re.compile('item\.jd\.com/.*'))
        for item in items:
            yield JdGoodsItem(goods_name=item.text,goods_link=item['href'])
        
        

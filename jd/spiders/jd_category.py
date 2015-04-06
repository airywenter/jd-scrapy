# -*- coding: utf-8 -*-
import re
import os
import scrapy
import logging
import random
import time
from xlsxwriter.workbook import Workbook
from bs4 import BeautifulSoup as Soup
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from jd.settings import DATA_DIR,FILTER_CATEGORIES


LOG=logging.getLogger(__name__)

class JdCategorySpider(CrawlSpider):
    name = "jd-category"
    allowed_domains = ["jd.com"]
    start_urls = (
        'http://www.jd.com/',
    )
    rules=(Rule(LinkExtractor(allow=('channel\.jd\.com/.*',)),callback='parse_items'),)

    def convert_item_url(self,item):
        if not item.get('href'):
            return
        item_id=re.search('\d+',item['href']).group()
        return 'http://wap.jd.com/comments/%s.html'%item_id
    
    def write_to_file(self,filename,items,fdir=DATA_DIR):
        fpath=os.path.join(fdir,filename)+'.txt'
        LOG.info('WRITTING TO PATH:::%s\n'%fpath)
        with open(fpath,'a') as f:
            for item in items:
                f.write(item.encode('utf-8').strip()+'\n')
    
    def write_to_excel(self,filename,items,fdir=DATA_DIR):
        fpath=os.path.join(fdir,filename+'.xlsx')
        workbook=Workbook(fpath)
        worksheet=workbook.add_worksheet()
        for i in range(len(items)):
            for j in range(len(items.split(':::'))):
                worksheet.write(i,j,items.split(':::')[j].decode('gbk'))
            

    def parse_items(self,response):
        s=Soup(response.body)
        items=s.find_all('a',href=re.compile('item\.jd\.com/.*'))
        items=filter(lambda x:len(x.text.strip())>1,items)
        items_save=[re.sub('\r|\n| |\t','',re.search('\d+',i['href']).group()+' ::: '+i.text.strip()) for i in items] 
        filename=re.search('jd\.com/(.*)\.',response.url).groups()[0]
        if len(FILTER_CATEGORIES)>0 and filename not in FILTER_CATEGORIES:
            return 
        self.write_to_file(filename, items_save)
        for item in items:
            time.sleep(random.randrange(0,3))
            yield scrapy.Request(self.convert_item_url(item),callback=lambda r :self.get_comments(r,item=item,category=filename))
            

    def get_comments(self,response,item,category,number=1):
        s=Soup(response.body)
        comments=s.find_all('div',class_='eval')
        all_comments=[]
        for comment in comments:
            user=comment.find('div',class_='u-info').text
            score=comment.find('div',class_='u-score').text
            content=comment.find('div',class_='u-summ').text
            comment=re.sub('\n| |\r|\t','',user+':::'+score+':::'+content)
            all_comments.append(comment)
        if not os.path.isdir(os.path.join(DATA_DIR,category)):
            os.mkdir(os.path.join(DATA_DIR,category))
        category_dir=os.path.join(DATA_DIR,category)
        filename=re.search('\d+',item['href']).group()
        self.write_to_file(filename, all_comments,category_dir)
        number+=1
        if number<10 and len(comments)>1:
            time.sleep(random.randrange(0,5))
            yield scrapy.Request(self.convert_item_url(item)+'?page=%d'%number,callback=lambda r:self.get_comments(r, item, category, number))
        
        

#             yield JdComment(comment_user=user,comment_score=score,comment_content=content)
            
            
            
            
            
        


    

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jd.spiders.jd_items import JdItemsSpider

class JdPipeline(object):
    
    def process_item(self, item, spider):
        print item
            
            
        
        
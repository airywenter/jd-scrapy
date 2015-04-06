# -*- coding: utf-8 -*-
import os

# Scrapy settings for jd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jd'

SPIDER_MODULES = ['jd.spiders']
NEWSPIDER_MODULE = 'jd.spiders'
USER_AGENT='Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

#ITEM_PIPELINES={'jd.pipelines.JdPipeline':  100}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jd (+http://www.yourdomain.com)'
if not os.path.exists(os.path.join(os.getcwd(),'data')):
    os.mkdir(os.path.join(os.getcwd(),'data'))

DATA_DIR=os.path.join(os.getcwd(),'data')

LOG_LEVEL = 'INFO'

FILTER_CATEGORIES=['beauty']
    
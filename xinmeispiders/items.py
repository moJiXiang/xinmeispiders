# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidersResultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    domain = scrapy.Field() # baidu.com / google.com
    kwid = scrapy.Field() # 关键字objectid
    kw = scrapy.Field() # 关键词
    title = scrapy.Field() # 标题
    url = scrapy.Field() # 链接
    brief = scrapy.Field() # 简介
    sourceurl = scrapy.Field() # 来源链接
    score = scrapy.Field() # 打分
    rank = scrapy.Field() # 排名



class StackItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()

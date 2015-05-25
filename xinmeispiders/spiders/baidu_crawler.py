# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
from datetime import datetime
from xinmeispiders.items import XinmeispidersItem
from xinmeispiders.db import db
import json
from bson import json_util
from bson.json_util import dumps



class BaiduCrawlerSpider(CrawlSpider):
    # start_urls = [
    name = 'baidu_crawler'
    allowed_domains = ['baidu.com']
    #     # "http://www.baidu.com/s?wd=%s" % kw.encode('gbk')
    # ]
    # , restrict_xpaths='//a[@class=n][last()]'
    # allow=r's\?wd=(%?.+?\d+?){0,}', 
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a[@class="n"][contains(., ">")]'),callback='parse_item', follow=True),
    )

    # def __init__(self):
    #     log_file = 'logs/scrapy_%s_%s.log' % (self.name, datetime.today())
    #     log.start(log_file, loglevel=log.INFO)
    #     log.msg('Baidu crawler begin run at [%s]' % datetime.today(), level=log.INFO)

    def get_kws_fromdb(self):
        searchwords = db["searchwords"]
        results = json.loads(dumps(searchwords.find({"isbdsearched": 0})), object_hook=json_util.object_hook)
        kws = []
        for re in results:
            kws.append(re['kw'])

        searchwords.update({"isbdsearched": 0}, {'$set': {'isbdsearched': 1}}, multi=True)
        
        return kws

    def start_requests(self):
        '''
            This method will use mongodb searchwords
            to init start urls
        '''
        kws = self.get_kws_fromdb()
        for kw in kws:
            yield self.make_requests_from_url("http://www.baidu.com/s?wd=%s" % kw.encode('gbk'))

    def make_requests_from_url(self, url):
        request = Request(url)
        return request

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        results = Selector(response).xpath('//div[contains(@class, "c-container") and not(contains(@class, "result-op"))]')
        kw = Selector(response).xpath('//input[@id = "kw"]/@value').extract()[0]
        for result in results:
            item = XinmeispidersItem()
            item['domain'] = self.allowed_domains[0]
            item['kw'] = kw
            item['title'] = result.xpath('string(.//h3//a)').extract()[0]
            item['url'] = result.xpath('.//h3/a/@href').extract()[0]
            item['brief'] = result.xpath('string(.//div[@class="c-abstract"])').extract()[0]
            yield item

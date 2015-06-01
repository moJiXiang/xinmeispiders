# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
from datetime import datetime
from xinmeispiders.items import SpidersResultItem
from xinmeispiders.db import db
import json
from bson import json_util
from bson.json_util import dumps
from urlparse import urlparse
import time

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
        self.searchwords = db["searchwords"]
        results = json.loads(dumps(self.searchwords.find({"isbdsearched": 0})), object_hook=json_util.object_hook)
        kws = []
        for re in results:
            kws.append(re['kw'])

        # searchwords.update({"isbdsearched": 0}, {'$set': {'isbdsearched': 1}}, multi=True)
        
        return kws

    def start_requests(self):
        '''
            This method will use mongodb searchwords
            to init start urls
        '''
        kws = self.get_kws_fromdb()
        for i, kw in enumerate(kws):
            second = i * 2
            time.sleep(second)
            yield self.make_requests_from_url("http://www.baidu.com/s?wd=%s" % kw.encode('gbk'), kw)

    def make_requests_from_url(self, url, kw):
        request = Request(url)
        return request

    def parse_start_url(self, response):
        self.searchwords.update({"isbdsearched": 0}, {'$set': {'isbdsearched': 1}}, multi=True)
        return self.parse_item(response)

    def parse_item(self, response):
        results = Selector(response).xpath('//div[contains(@class, "c-container") and not(contains(@class, "result-op"))]')
        kw = Selector(response).xpath('//input[@id = "kw"]/@value').extract()[0]
        current_page = Selector(response).xpath('string(//div[@id="page"]//strong//span[@class="pc"])').extract()[0]
        for i, result in enumerate(results):
            item = SpidersResultItem()
            item['domain'] = self.allowed_domains[0]
            item['kwid'] = ''
            item['kw'] = kw
            item['title'] = result.xpath('string(.//h3//a)').extract()[0]
            item['url'] = result.xpath('.//h3/a/@href').extract()[0]
            item['brief'] = result.xpath('string(.//div[@class="c-abstract"])').extract()[0]
            urlstr = 'http://' + result.xpath('string(.//div[@class="f13"]//span)').extract()[0]
            parsed_uri = urlparse(urlstr)
            item['sourceurl'] = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            item['score'] = 0

            # 根据active的a标签的值来排名
            if current_page:
                page = current_page if int(current_page) >= 10 else ('0%s' % (current_page,))
            else:
                page = '01'
            rank = str(i) if i >= 10 else ('0%d' %(i,)) 
            item['rank'] = page + rank
            item['content'] = ''
            yield item

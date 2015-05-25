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


class GoogleCrawlerSpider(CrawlSpider):
    name = 'google_crawler'
    allowed_domains = ['google.com']
    # start_urls = ['http://www.google.com/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a[@id="pnnext"]'), callback='parse_item', follow=True),
    )

    def get_kws_fromdb(self):
        searchwords = db["searchwords"]
        results = json.loads(dumps(searchwords.find({"isglsearched": 0})), object_hook=json_util.object_hook)
        kws = []
        for re in results:
            kws.append(re['kw'])

        searchwords.update({"isglsearched": 0}, {'$set': {'isglsearched': 1}}, multi=True)
        
        return kws

    def start_requests(self):
        '''
            This method will use mongodb searchwords
            to init start urls
        '''
        kws = self.get_kws_fromdb()
        for kw in kws:
            yield self.make_requests_from_url("https://www.google.com/search?q=%s" % kw.encode('utf8'))

    def make_requests_from_url(self, url):
        request = Request(url)
        return request

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        results = Selector(response).xpath('//div[@class="rc"]')
        kw = Selector(response).xpath('//input[@id="lst-ib"]/@value').extract()[0]
        hasResult = Selector(response).xpath('string(//div[@class="med"])').extract()[]
        if not hasResult:
            for result in results:
                item = XinmeispidersItem()
                item['domain'] = self.allowed_domains[0]
                item['kw'] = kw
                item['title'] = result.xpath('string(.//h3//a)').extract()[0]
                item['url'] = result.xpath('./h3/a/@href').extract()[0]
                item['brief'] = result.xpath('string(.//span[@class="st"])').extract()[0]
                yield item
        else:
            pass
        

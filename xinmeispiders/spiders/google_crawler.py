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
        hasResult = Selector(response).xpath('//div[@id="topstuff"]//div[@class="med"]')
        if len(hasResult)>0:
            searchwords.update({"isglsearched": 0}, {'$set': {'isglsearched': 1}}, multi=True)
        else:
            return self.parse_item(response)

    def parse_item(self, response):
        results = Selector(response).xpath('//div[@class="rc"]')
        kw = Selector(response).xpath('//input[@id="lst-ib"]/@value').extract()[0]
        current_page = Selector(response).xpath('string(//td[@class="cur"])').extract()[0]
        for i, result in enumerate(results):
            item = SpidersResultItem()
            item['domain'] = self.allowed_domains[0]
            item['kwid'] = ''
            item['kw'] = kw
            item['title'] = result.xpath('string(.//h3//a)').extract()[0]
            item['url'] = result.xpath('./h3/a/@href').extract()[0]
            item['brief'] = result.xpath('string(.//span[@class="st"])').extract()[0]
            parsed_uri = urlparse(item['url'])
            item['sourceurl'] = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            item['score'] = 0

            # 根据active的a标签的值来排名
            if current_page:
                page = current_page if int(current_page) >= 10 else ('0%s' % (current_page,))
            else:
                page = '01'
            rank = str(i) if i >= 10 else ('0%d' %(i,)) 
            item['rank'] = page + rank
            yield item
        

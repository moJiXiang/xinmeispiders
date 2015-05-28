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


class SogouCrawlerSpider(CrawlSpider):
    name = 'sogou_crawler'
    allowed_domains = ['sogou.com']
    # start_urls = ['http://www.weixin.sogou.com/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a[@id="sogou_next"]'), callback='parse_item', follow=True),
    )

    def get_kws_fromdb(self):
        searchwords = db["searchwords"]
        results = json.loads(dumps(searchwords.find({"issgsearched": 0})), object_hook=json_util.object_hook)
        kws = []
        for re in results:
            kws.append(re['kw'])

        # searchwords.update({"issgsearched": 0},{'$set':{'issgsearched': 1}},multi=True)

        return kws
        
    def start_requests(self):
        kws = self.get_kws_fromdb()
        for kw in kws:
            yield self.make_requests_from_url("http://weixin.sogou.com/weixin?type=2&fr=sgsearch&query=%s" % kw.encode('gbk'))

    def make_requests_from_url(self, url):
        request = Request(url)
        return request

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        results = Selector(response).xpath('//div[@class="txt-box"]')
        kw = Selector(response).xpath('//input[@id="upquery"]/@value').extract()[0]
        current_page = Selector(response).xpath('string(//div[@id="pagebar_container"]/span)').extract()[0]
        for i, result in enumerate(results):
            item = SpidersResultItem()
            item['domain'] = self.allowed_domains[0]
            item['kwid'] = ''
            item['kw'] = kw
            item['title'] = result.xpath('string(.//h4//a)').extract()[0]
            item['url'] = result.xpath('.//h4//a/@href').extract()[0]
            item['brief'] = result.xpath('string(.//p)').extract()[0]
            item['sourceurl'] = 'http://mp.weixin.qq.com/'
            item['score'] = 0
            # 根据active的a标签的值来排名
            page = current_page if int(current_page) >= 10 else ('0%s' % (current_page,))
            rank = str(i) if i >= 10 else ('0%d' %(i,)) 
            item['rank'] = page + rank
            yield item





# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from xinmeispiders.items import XinmeispidersItem


class SogouCrawlerSpider(CrawlSpider):
    name = 'sogou_crawler'
    allowed_domains = ['weixin.sogou.com']
    # start_urls = ['http://www.weixin.sogou.com/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a[@id="sogou_next"]'), callback='parse_item', follow=True),
    )

    def get_kws_fromdb(self):
        searchwords = db["searchwords"]
        results = json.loads(dumps(searchwords.find({"status": 0})), object_hook=json_util.object_hook)
        
    def parse_item(self, response):
        i = XinmeispidersItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

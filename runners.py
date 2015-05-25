#!/usr/bin/python
# -*- coding: utf-8 -*-
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from xinmeispiders.spiders.baidu_spider import BaiduSpider
from db import db
import json
import random
from bson import json_util
from bson.json_util import dumps


# def spider_closing(spider):
# 	"""Activates on spider closed signal"""
# 	log.msg("Closing reactor", level=log.INFO)
# 	reactor.stop()

def setup_crawler(keywords):
	spider = BaiduSpider(keywords = keywords)
	settings = get_project_settings()
	crawler = Crawler(settings)
	# stop reactor when spider closes
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()
	log.start(loglevel = log.DEBUG)
	reactor.run()

searchwords = db["searchwords"]
results = json.loads(dumps(searchwords.find({"status": 0})), object_hook=json_util.object_hook)
kws = []
for re in results:
	str = '"%s %s"'%(re['main'], re['keyword'],) 
	kws.append(str)
# kws.append('"%s %s %s"'%(kw['main'], kw['keyword'], kw['word']) for kw in results)
# kws = [u'"中新恒超 裁判文书"', u'"中新恒超 法人"']
# for kw in kws:
# 	setup_crawler(kw)
setup_crawler(kws)
# -*- coding: utf-8 -*-
from datetime import date
import json
import random
from bson import json_util
from bson.json_util import dumps
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import os
import logging
from db import db
from twisted.internet import reactor
from scrapy import signals, log
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from xinmeispiders.spiders.baidu_spider import BaiduSpider
# 设置默认的log文件
logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG)

searchwords = db["searchwords"]

executors = {
	'default': ThreadPoolExecutor(20),
	'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
	'coalesce': False
}

scheduler = BlockingScheduler(executors = executors, job_defaults = job_defaults)

def setup_crawler(keyword):
	print 'schedule run script is running.........'
	spider = BaiduSpider(keyword = keyword)
	settings = get_project_settings()
	crawler = Crawler(settings)
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()
	log.start(loglevel = log.DEBUG)
	reactor.run()

def run_spiders():
	results = json.loads(dumps(searchwords.find({"status": 0})), object_hook=json_util.object_hook)
	length = len(results)
	searchword = results[random.randint(0, length - 1)]

	keyword = ['"%s %s %s"'%(searchword['main'], searchword['keyword'], searchword['word'])]
	# keyword = [u'"中新恒超 裁判文书"']
	print keyword
	setup_crawler(keyword[0])
	# log.start(loglevel = log.DEBUG)
scheduler.add_job(run_spiders, 'interval', seconds=20)
scheduler.start()

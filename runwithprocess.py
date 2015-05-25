# -*- coding: utf-8 -*-
# from celery import task
from multiprocessing.queues import Queue
from scrapy import log, signals, project
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
# from scrapy.spider import BaseSpider
import multiprocessing

class CrawlerWorker(multiprocessing.Process):

	def __init__(self, spider, result_queue):
		multiprocessing.Process.__init__(self)
		self.result_queue = result_queue

		self.crawler = CrawlerProcess(settings)
		if not hasattr(project, 'crawler'):
			self.crawler.install()
		self.crawler.configure()

		self.items = []
		self.spider = spider
		dispatcher.connect(self._item_passed, signals.item_passed)

	def _item_passed(self, item):
		self.items.append(item)

	def run(self):
		self.crawler.crawl(self.spider)
		self.crawler.start()
		self.crawler.stop()
		self.result_queue.put(self.items)










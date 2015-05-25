#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.exceptions import DropItem
from scrapy import log

class MongoDBPipeline(object):

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri = crawler.settings.get('MONGO_URI'),
			mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		log.msg("Change search words status!", level=log.DEBUG, spider=spider)

		self.client.close()

	def process_item(self, item, spider):
		# for data in item:
		# 	if not data:
		# 		raise DropItem("Missing data!")
		collection_name = item.__class__.__name__
		self.db[collection_name].update({'url': item['url']}, dict(item), upsert=True)
		log.msg("Added to MongoDB database!", level=log.DEBUG, spider=spider)

		return item
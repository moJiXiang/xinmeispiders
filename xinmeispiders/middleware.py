#-*-coding:utf-8-*-
import random
import re
from scrapy import log
from scrapy.exceptions import IgnoreRequest

class RandomUserAgent(object):
	"""Randomly rotate user agents based on a list of setting files"""

	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))

	def process_request(self, request, spider):
		request.headers.setdefault('User-Agent', random.choice(self.agents))
		spider.log(
			u'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request),
			level = log.DEBUG
		)

class ProxyMiddleware(object):
	"""Random proxy from proxies.txt"""
	filename = "proxies.txt"

	def process_request(self, request, spider):
		with open(self.filename, 'r') as proxiesfile:
			proxies = proxiesfile.read().replace('/n','')

		r = re.compile(u'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,}')
		proxies = r.findall(proxies)
		# Set the location of the proxy
		proxy_string = random.choice(proxies)
		request.meta['proxy'] = "http://%s" % proxy_string
		spider.log(
			u'proxy: {}'.format(request.meta.get('proxy')),
			level = log.DEBUG
		)

	def process_exception(self, request, exception, spider):
		proxy = request.meta['proxy']
		log.msg('Removing failed proxy <%s>' % (
			proxy,))
		try:
			del self.proxies[proxy]
		except ValueError:
			pass
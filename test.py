# -*- coding: utf-8 -*-
import re
from scrapy.http import Request
# url = 'http://www.baidu.com/link?url=WSXYV9Ezz7Pbt3QiaDeT-jUrWaO-r-aKixuYyj-GHqHEEewpziXzb4vA5lQWB1nfBO1ztJAj4x9FjVwHvxFmiAlXoDzhC_FzHsP8CBlgWGa'
# request = Request(url)
# print request.meta
# print request.url
# print request.headers

# from urlparse import urlparse
# parsed_uri = urlparse('news.yxlady.com/201505... ')
# domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
# print domain

# str = u'国家统计局27日发布的数据显示,2013年全国城镇非私营单位就业人员年平均工资51474元,同比名义增长10.1%,扣除物价因素实际增长7.3%,增速较上年有所回落.'
# title = u'统计局:2013年全国平均工资统计_中国行业研究网'
# kw = u'去年全国平均工资'

# r = re.compile(kw)
# matchs = r.search(title)
# print matchs.group()
ints = [8, 23, 45, 12, 78]
for i, num in enumerate(ints):
	print i
	print num
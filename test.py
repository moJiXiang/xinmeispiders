#!/usr/bin/python
# import re

# url = '/s?wd=%96%B0%E9%97%BB&amp;pn=10&am'

# # r = re.compile(r's\?wd=(%?.+?\d+?){0,}')
# r = re.compile(r's\?wd=.{0,}')

# matchs = r.search(url)

# print matchs.group()

arr = [{"name": "mojixang"}, {"name": "qiqiu"}]

kws = []
for kw in arr:
	str = kw["name"]
	kws.append(str)
# kws.append(kw for kw in arr)
print kws
# -*- coding:utf-8 -*-
from pymongo import MongoClient
# 链接数据库
# client = MongoClient("localhost:27017")
client = MongoClient("mongodb://xinmei:xinmei@117.121.25.124:27017/xinmei-development")
db = client["xinmei-development"]
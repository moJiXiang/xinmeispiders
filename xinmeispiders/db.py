# -*- coding:utf-8 -*-
from pymongo import MongoClient
# 链接数据库
client = MongoClient("mongodb://localhost:27017")
db = client["xinmei-development"]
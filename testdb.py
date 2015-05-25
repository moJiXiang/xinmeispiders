#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import db
import time
from datetime import datetime
times = db["times"]

today = {'date': datetime.today()}
times.insert(today)
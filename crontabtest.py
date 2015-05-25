# -*- coding: utf-8 -*-
from crontab import CronTab

empty_cron = CronTab()
my_cron = CronTab(user=True)
user_cron = CronTab(user="mojixiang")
# tab = CronTab(user="mojixiang")
cmd = '/usr/bin/python /Users/mojixiang/Works/xinmeispiders/runner.py'

cron_job = user_cron.new(cmd, comment="This is the main command")
cron_job.minute().every(1)

user_cron.write()
print user_cron.render()
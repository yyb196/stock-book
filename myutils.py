#!/usr/bin/env python
# encoding: utf-8
"""
myutils.py

Created by yang frank on 2010-10-10.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from google.appengine.api import urlfetch
from google.appengine.api import users
import logging

PER_PRICE_COUNT = 10
PER_PAGE_COUNT = 6#20
CACHE_TIME_SECOND = 3600*2
STOCK_PER_FETCH_SIZE = 1000#1000

current_id=0

def sameDay(dayOne, dayTwo):
	if dayOne == dayTwo:
	    return True
	return False

def getStockPrice(stock_id):
    prefix="sh"
    if stock_id[0] == '0':
        prefix = "sz"
	
	logging.debug('get stock from sina,stock id'+stock_id)
    url='http://hq.sinajs.cn/list='+prefix+stock_id
    result = urlfetch.fetch(url)
    logging.debug('get stock from sina,stock id'+stock_id + 'result is :' \
                 + str(result.status_code))
    if result.status_code == 200:
        return result.content.split('"')[1]
    return ""

def cntime():
	return datetime.datetime.utcnow() + datetime.timedelta(hours=+8)

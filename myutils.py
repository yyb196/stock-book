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
import re
PER_PRICE_COUNT = 10
PRICE_LINES = 4
PER_PAGE_COUNT = 6#20
CACHE_TIME_SECOND = 3600*2
STOCK_PER_FETCH_SIZE = 1000#1000

current_id=0
SID_PAT = re.compile(r'.*(_sh|_sz)(\d{6})=.*')
SUB_PAT = re.compile(r'(\n|\r)+')

def sameDay(dayOne, dayTwo):
	if dayOne == dayTwo:
	    return True
	return False

def getStockPrice(stock_id):
    prefix="sz"
    if stock_id[0] == '6':
        prefix = "sh"
	
	logging.debug('get stock from sina,stock id'+stock_id)
    url='http://hq.sinajs.cn/list='+prefix+stock_id
    result = urlfetch.fetch(url)
    logging.debug('get stock from sina,stock id'+stock_id + 'result is :' \
                 + str(result.status_code))
    if result.status_code == 200:
        return result.content.split('"')[1]
    return ""

def getStockPrices(sidArr):
    logging.error("start get price from sina stock.")
    newArr = [(sid.stock_id[0] == '6' and 'sh' or 'sz') + sid.stock_id for sid in sidArr]
    params = ",".join(newArr)
    url='http://hq.sinajs.cn/list='+params
    result=urlfetch.fetch(url)
    logging.debug('get stock from sina,stock id '+params + 'result is :' \
                 + str(result.status_code))
    map={}
    if result.status_code == 200:
        for line in SUB_PAT.sub('', result.content.decode('gb2312')).split(";"):
            if len(line.strip()) > 10:
                commaArr = line.split('"')
                sid=SID_PAT.match(commaArr[0]).group(2)
                detail=commaArr[1]
                map[sid]=(detail.split(',')[3], detail)
    logging.error("finished get price from sina stock.")
    return map



def cntime():
	return datetime.datetime.utcnow() + datetime.timedelta(hours=+8)

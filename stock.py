#!/usr/bin/env python
# encoding: utf-8
"""
stock.py

Created by yang frank on 2010-10-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import logging#

import myutils#

from google.appengine.ext import db#
import cacheMgr
import datetime#

def getStocks():
	stocks = cacheMgr.getStocks()
	logging.debug("get stocks from cache, stocks== null is %s" \
	             % (str(stocks==None)))
	if stocks == None:
		logging.debug('get stocks from db.')
		stocks = []
		next = True
		lastdatetime = datetime.datetime(2000, 1, 1, 21, 0, 0, 0)
		while next:
			query = Stock.gql("where datetime>:1 order by datetime asc", \
			           lastdatetime).fetch(myutils.STOCK_PER_FETCH_SIZE)
			next = len(query) == myutils.STOCK_PER_FETCH_SIZE
			if next:
				lastdatetime = query[myutils.STOCK_PER_FETCH_SIZE-1].datetime
			logging.debug("get stock size:" + str(len(query)))
			for one in query:
				stocks.append(one)
				t_now = (datetime.datetime.now()-one.datetime).seconds
				if t_now < 1:
					logging.error(one.stock_id + " is set datetime now")
					one.datetime=datetime.datetime.now() + \
			       	datetime.timedelta(microseconds=myutils.current_id)
					myutils.current_id = myutils.current_id + 1
					one.put()
		logging.debug('get stocks from db, size is %s' % (str(len(stocks))))
		#cache 2 hours
		cacheMgr.cacheStocks(stocks)
		setStockCountToMem(len(stocks))
	return stocks

def getStockCount():
	c = cacheMgr.getStockCount()
	if c:
		return c
	c = len(getStocks())
	setStockCountToMem(c)
	return c

def setStockCountToMem(count):
	cacheMgr.cacheStockCount(count)

class Stock(db.Model):
    stock_id = db.StringProperty(required=True)
    name = db.StringProperty()
    creater = db.StringProperty()
    date = db.DateProperty(auto_now_add=True)
    price_update_date = db.DateProperty()
    datetime = db.DateTimeProperty(auto_now_add=True)




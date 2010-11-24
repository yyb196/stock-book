#!/usr/bin/env python
# encoding: utf-8
"""
cacheMgr.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import myutils
import stock
from google.appengine.api import memcache

def cachePageContent(page, isAdmin, prefix, content):
	memcache.set("content" + str(page) + str(isAdmin) + prefix, content, 120)

def delPageContent():
	pageNum = (stock.getStockCount()+myutils.PER_PAGE_COUNT-1)/myutils.PER_PAGE_COUNT
	for i in range(0, pageNum):
		for s in ['True', 'False']:
			for p in ['/', '/fav/']:
				memcache.delete("content" + str(i) +s+p)
				

def getPageContent(page, isAdmin, prefix):
	return memcache.get("content" + str(page) + str(isAdmin))

def cacheUsers(userList):
	memcache.set("authenUsers", userList, 1000)

def getUsers():
	return memcache.get("authenUsers")

def cacheStocks(stocks):
	memcache.set("stocks", stocks, myutils.CACHE_TIME_SECOND)

def getStocks():
	return memcache.get("stocks")

def cacheStockCount(count):
	memcache.set("stocksCounts", count, 3600*24*5)

def getStockCount():	
	return memcache.get("stocksCounts")

def cacheLastComment(sid, comment):
	memcache.set("last_comment" + sid, comment, myutils.CACHE_TIME_SECOND)

def getLastComment(sid):
	return memcache.get("last_comment" + sid)

def cacheStockPrice(sid, priceList):
	memcache.set("price"+sid, priceList, myutils.CACHE_TIME_SECOND)

def getStockPrice(sid):
	return memcache.get("price"+sid)

def cacheFavStocks(name, result):
	memcache.set(name + "favStocks", result, myutils.CACHE_TIME_SECOND)

def getFavStocks(name):
	return memcache.get(name + "favStocks")

def triggerAddStock(stock):
	memcache.delete('stocks')
	delPageContent()

def triggerAddComment(sid, stockComment):
	memcache.set("last_comment" + sid, stockComment, myutils.CACHE_TIME_SECOND)
	delPageContent()

def triggerDelStock(stock):
	memcache.delete('stocks')
	delPageContent()

def triggerUpdateStock(stocks, stock, price):
	memcache.delete('stocks')
	memcache.delete("price"+stock.stock_id)
	delPageContent()

def triggerUserChange():
	memcache.delete("authenUsers")


def triggerUpdateStocks(stocks):
	memcache.delete('stocks')
	for s in stocks:
		memcache.delete("price"+s.stock_id)	
	delPageContent()	





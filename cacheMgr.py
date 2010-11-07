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

def cachePageContent(page, isAdmin, content):
	memcache.set("content" + str(page) + str(isAdmin), content, 120)

def delPageContent():
	pageNum = (stock.getStockCount()+myutils.PER_PAGE_COUNT-1)/myutils.PER_PAGE_COUNT
	for i in range(0, pageNum):
		memcache.delete("content" + str(i) +"True")
		memcache.delete("content" + str(i) +"False")

def getPageContent(page, isAdmin):
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
	memcache.get("last_comment" + sid)

def cacheStockPrice(sid, priceList):
	memcache.set("price"+sid, priceList, myutils.CACHE_TIME_SECOND)

def getStockPrice(sid):
	memcache.get("price"+sid)

def triggerAddStock(stock):
	memcache.delete('stocks')
	delPageContent()

def triggerAddComment(sid, stockComment):
	memcache.set("last_comment" + sid, stockComment.comment, myutils.CACHE_TIME_SECOND)
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






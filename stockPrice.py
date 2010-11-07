#!/usr/bin/env python
# encoding: utf-8
"""
stockPrice.py

Created by yang frank on 2010-10-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.ext import db#
import logging#
import myutils#
import cacheMgr

class StockPrice(db.Model):
    stock_id = db.StringProperty(required=True)
    price = db.StringProperty(required=True)
    detail = db.StringProperty(required=True)
    date = db.DateProperty(auto_now_add=True)

def getPriceList(stock_id):
    priceList = cacheMgr.getStockPrice(stock_id)
    logging.debug("get price from cache for price%s is None? %s" % (stock_id, \
                  str(priceList == None)))
    if priceList:
        return priceList
    query = StockPrice.gql("WHERE stock_id=:1 order by date desc",
		                                stock_id)
    query = query.fetch(limit=myutils.PER_PRICE_COUNT)
    logging.debug("get price for %s , count is: %s" % (stock_id, str(len(query))))
    cacheMgr.cacheStockPrice(stock_id, query)
    return query

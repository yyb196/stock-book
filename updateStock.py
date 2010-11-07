#!/usr/bin/env python
# encoding: utf-8
"""
updateStock.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import logging#

import myutils#
from google.appengine.ext import webapp#

from datetime import date#
import datetime#
import stock#
from stockPrice import StockPrice#
import cacheMgr

class UpdateStock(webapp.RequestHandler):
    def get(self):
        h = datetime.datetime.utcnow().hour
        logging.debug("update stock hour is:" + str(h))
        if h >= 8 and h < 16:
            stocks = stock.getStocks()
            today = date.today()
            for one in stocks:
                if myutils.sameDay(today, one.price_update_date):
                    pass
                else:
                    stock_detail_str = myutils.getStockPrice(one.stock_id).decode('gb2312')
                    stock_detail = StockPrice(stock_id=one.stock_id, \
		    	                         detail=stock_detail_str, \
		    	                         price=stock_detail_str.split(',')[3])
                    stock_detail.put()
                    one.price_update_date = today
                    one.put()
                    cacheMgr.triggerUpdateStock(stocks, one, stock_detail)
        
        self.redirect("/")



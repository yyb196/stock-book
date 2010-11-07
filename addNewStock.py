#!/usr/bin/env python
# encoding: utf-8
"""
addNesStock.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import logging#
import myutils#
import myaop#

from google.appengine.ext import webapp#
from google.appengine.api import users#
import stock as stockUtils#
from stock import Stock#
from stockPrice import StockPrice#
import cacheMgr
from datetime import date#
import datetime

class AddNewStock(webapp.RequestHandler):
    @myaop.admin()
    def post(self):
        stockValue = self.request.get('stock_value')
        stocks = stockUtils.getStocks()
        hasSame = False
        for s in stocks:
	        if s.stock_id == stockValue:
		        hasSame = True
		logging.info("add stock with id %s and has same is %s" \
		           % (stockValue, str(hasSame)))
		if hasSame:
			self.redirect('/')
			return
        stock = Stock(stock_id=stockValue, \
                    creater=users.get_current_user().email())
        stock_detail_str = myutils.getStockPrice(stockValue).decode('gb2312')
        if stock_detail_str != '':
            stock_detail_list = stock_detail_str.split(',')
            stock.name=stock_detail_list[0]
            stock.price_update_date=date.today()
            stock.put()
            stock_detail = StockPrice(stock_id=stockValue, \
                              price=stock_detail_list[3], \
                              detail=stock_detail_str)
            stock_detail.put()
        
        #update stocks cache
        cacheMgr.triggerAddStock(stock)
        self.redirect('/')


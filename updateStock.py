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
from google.appengine.ext import db
from datetime import date#
import datetime#
import stock#
from stockPrice import StockPrice#
import cacheMgr

class UpdateStock(webapp.RequestHandler):
    def get(self):
        h = datetime.datetime.utcnow().hour
        logging.debug("update stock hour is:" + str(h))
        if h >= 8 and h < 16:#8+8 16+8
            stocks = stock.getStocks()
            today = date.today()
            sArr = []
            for one in stocks:
                if myutils.sameDay(today, one.price_update_date):
                    pass
                else:
                    sArr.append(one)
                    if len(sArr)>=40:
                        break
            if len(sArr) > 0:
                resultMap=myutils.getStockPrices(sArr)
                priceArr = []
                
                for t in sArr:
                    result = resultMap[t.stock_id]
                    stockPrice = StockPrice(stock_id=t.stock_id,\
                               detail=result[1], \
                                price=result[0])
                    priceArr.append(stockPrice)
                    t.price_update_date = today
                db.put(priceArr)
                db.put(sArr)       
                cacheMgr.triggerUpdateStocks(stocks)
        self.redirect("/")



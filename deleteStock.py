#!/usr/bin/env python
# encoding: utf-8
"""
deleteStock.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import myaop#
import logging#
from stock import Stock#
from google.appengine.ext import webapp#
import cacheMgr

class DeleteStock(webapp.RequestHandler):
	@myaop.admin()
	def get(self):
		sid = self.request.get('sid')
		stock = Stock.gql("where stock_id=:1", sid).fetch(1)
		stock = len(stock) == 1 and stock[0] or None
		if stock:
			logging.info("delete one stock with id " + sid)
			stock.delete()
			cacheMgr.triggerDelStock(stock)
		self.redirect('/')


#!/usr/bin/env python
# encoding: utf-8
"""
addStockComment.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import logging
import myaop#
import myutils
from google.appengine.ext import webapp#
from google.appengine.api import users#
from stockComment import StockComment#
import cacheMgr

class AddStockComment(webapp.RequestHandler):
	@myaop.admin()
	def post(self):
		sid = self.request.get('stock_id')
		c = self.request.get('comment')
		name = users.get_current_user().email()
		logging.info("add new commonet for stock:%s, by %s" % (sid, name))
		stockComment = StockComment(stock_id=sid, comment=c, creator=name)
		stockComment.put()
		cacheMgr.triggerAddComment(sid, stockComment)
		self.redirect('/')

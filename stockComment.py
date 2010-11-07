#!/usr/bin/env python
# encoding: utf-8
"""
stockComment.py

Created by yang frank on 2010-10-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.ext import db#
import logging#
import myutils#
import cacheMgr

def getLastComment(stock_id):
	last_comment = cacheMgr.getLastComment(stock_id)
	logging.debug("get last comment from cache for last_comment%s isNone? %s" \
	             % (stock_id, str(last_comment == None)))
	if last_comment:
		return last_comment
	query = StockComment.gql("where stock_id=:1 order by date desc", stock_id).\
	          fetch(1)
	last_comment = len(query) == 1 and query[0] or None
	logging.debug("get last comment from db for last_comment%s is %s" \
	              % (stock_id, str(last_comment)))
	if last_comment:
		cacheMgr.cacheLastComment(stock_id, last_comment)
	return last_comment


class StockComment(db.Model):
	stock_id = db.StringProperty(required=True)
	comment = db.TextProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)

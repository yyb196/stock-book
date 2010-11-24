#!/usr/bin/env python
# encoding: utf-8
"""
favorateStock.py

Created by yang frank on 2010-11-07.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import logging
import myaop#
import myutils
from google.appengine.ext import webapp#
from google.appengine.api import users#
import cacheMgr
from google.appengine.ext import db#

def getFavStocks(name):
	q = cacheMgr.getFavStocks(name)
	if q and len(q)>0:
		return q
	q = FavModel.gql("where name=:1 order by datetime desc", name).fetch(500)
	size = len(q)
	while size == 201:
		r = FavModel.gql("where name=:1 and datetime<:2 order by datetime desc",
		        name, q[len(q)-1] )
		size = len(r)
		if size > 0:
			q = q + r;
	cacheMgr.cacheFavStocks(name, q)
	return q

class FavStockAction(webapp.RequestHandler):
	@myaop.admin()
	def post(self, op, sid):
		name = users.get_current_user().email()
		logging.info("%s fav stock for %s, stock id: %s" % (op, name, sid))
		q = FavModel.gql("where name=:1 and stock_id=:2", name, sid).fetch(1)
		if op == 'add':
			if len(q) < 1:	
				fav = FavModel(name=name, stock_id=sid)
				fav.put()
				arr = cacheMgr.getFavStocks(name)
				if arr:
					arr.append(fav)
					cacheMgr.cacheFavStocks(name, arr)	
		elif op == 'delete':
			if len(q) > 0:
				q[0].delete()
				arr = cacheMgr.getFavStocks(name)
				if arr :
					toDel = None
					for a in arr:
						if a.stock_id == q[0].stock_id:
							toDel = a
					if toDel:
						arr.remove(toDel)
					cacheMgr.cacheFavStocks(name, arr)
		
		self.response.out.write("ok")


class FavModel(db.Model):
	stock_id = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	datetime = db.DateTimeProperty(auto_now_add=True)

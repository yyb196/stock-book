#!/usr/bin/env python
# encoding: utf-8
"""
nextComment.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import myaop#
import logging
from google.appengine.ext import webapp#
import datetime
from stockComment import StockComment
import cgi#
import urllib

class NextComment(webapp.RequestHandler):
	@myaop.admin()
	def get(self, sid, d):
		d = urllib.unquote_plus(d)
		arr = d.split('+')
		d = " ".join(arr)
		arr = d.split('.')
		logging.info("next comment params %s, %s, %s" % (sid, arr[0], arr[1]))
		
		dt = datetime.datetime.strptime(arr[0], '%Y-%m-%d %H:%M:%S')
		dt.replace(microsecond=int(arr[1]))
		query = StockComment.gql("where stock_id=:1 and date<:2 order by date desc", sid, dt).fetch(1)
		if len(query) == 1:
			comment = query[0]
			self.response.out.write("<div style=\"word-break:break-all; word-wrap:break-all;\" \
			  title=\"%s\">%s</div><div><input type=\"button\" value=\"Next\" \
			  onclick=\"nextComment('%s', '%s')\" /></div>" \
			 % (urllib.quote_plus(str(comment.date)), 
			     cgi.escape(comment.comment), sid, urllib.quote_plus(str(comment.date))))
		else:
			logging.info("has no comment for " + sid)
			self.response.out.write("None")

#!/usr/bin/env python
# encoding: utf-8
"""
pageStockModel.py

Created by yang frank on 2010-10-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import myutils

class PageStockModel():
	def __init__(self):
		self.stock_id=""
		self.stock_name=""
		self.stock_price_list = []
		self.href='#'
		self.last_comment = ("","","","")
		self.high_light = False
		for i in range(0, myutils.PER_PRICE_COUNT):
			self.stock_price_list.append(CellModel('88888888',\
			                       "2007-10-10"))

class CellModel():
	def __init__(self, p, d):
		self.price=p
		self.date=d
		self.color="red"

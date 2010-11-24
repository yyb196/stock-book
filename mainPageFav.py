#!/usr/bin/env python
# encoding: utf-8
"""
mainPageFav.py

Created by yang frank on 2010-11-07.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import mainPage

class MainPageFav(mainPage.MainPage):
	def getPrefix(self):
		return "/fav/"
	
	def getData(self, username):
		favList = self.getFavList(username)
		return [s for s in super(MainPageFav, self).getData(username) if s.stock_id in favList]
	
	def isNormal(self):
		return False
	



				

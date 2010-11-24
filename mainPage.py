#!/usr/bin/env python
# encoding: utf-8
"""
mainPage.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import stockPrice#
import cgi#
import os#
import logging#

import myutils#
import security#
from google.appengine.api import users#
from google.appengine.ext import webapp#
from google.appengine.ext.webapp import template#

import stock#
import stockComment#
import favorateStock#
from pageStockModel import PageStockModel#
from pageStockModel import CellModel#
import cacheMgr
import urllib

class MainPage(webapp.RequestHandler):
    def getUserInfo(self):
        user=users.get_current_user()
        isAdmin = False
        username = ""
        url = ""
        url_linktext = ""
        if user and security.checkUserAuth(user):
            url = users.create_logout_url("/")
            username = user.email()
            url_linktext = 'Logout'
            isAdmin = True
        if not user:
            url = users.create_login_url("/")
            username = "Anonymous"
            url_linktext = 'Login with google account'
        logging.debug("user is %s, isAdmin:%s" % (username, str(isAdmin)))
        return (isAdmin, username, url, url_linktext)
		
	
    def getData(self, username):
        return stock.getStocks()
	
	
    def getPageInfo(self, stocks, page, q, prefix):
        totalCount = len(stocks)
        light_stock_id = None
        if page==0 and q:
			findq = False
			while not findq:
				start  = page * myutils.PER_PAGE_COUNT
				end = start + myutils.PER_PAGE_COUNT
				islast = False
				if end >= totalCount:
					end = totalCount
					islast = True
				for one in stocks[start:end]:
					if one.name.find(q) != -1 \
			             or one.stock_id.find(q) != -1:
						findq=True
						light_stock_id = one.stock_id
						break
				page = findq and page or page + 1
				if islast:
					break
        if q and not light_stock_id:#search, no matched result,turn to first page
			page = 0
        
        start = page * myutils.PER_PAGE_COUNT
        if start >= len(stocks):
	        page = 0
	        start = 0
        end = start + myutils.PER_PAGE_COUNT
        hasNext = True
        hasPre = page > 0
        nextHref = prefix + "?page="+str(page+1)
        preHref = prefix + "?page="+str(page-1)
        if end >= totalCount:
            end = totalCount
            hasNext = False
        logging.debug("get stock from %s to %s" % (str(start), str(end)))
        return (page, light_stock_id, start, end, hasPre, hasNext, nextHref, preHref, totalCount)
	
    def getContent(self, stocks, start, end, light_stock_id, username):
        stockModelList=[]
        colTitles=[]
        favList = self.getFavList(username)
        for one in stocks[start:end]:
            stock_id = one.stock_id
            priceList = stockPrice.getPriceList(stock_id)
            comment = stockComment.getLastComment(stock_id)
            model = PageStockModel()
            model.stock_name = one.name
            model.stock_id = stock_id
            if model.stock_id in favList:
                model.isFav = True
            if comment:
                #logging.error("comment is:" + comment.comment)
                model.last_comment = (cgi.escape(comment.comment), \
                         urllib.quote_plus(str(comment.date)), comment.stock_id)
            if light_stock_id and light_stock_id == stock_id:
				model.high_light = True
			
            stockModelList.append(model)
            tmpIndex = myutils.PER_PRICE_COUNT*myutils.PRICE_LINES - 1
            lastprice = None
            #priceList is order by date desc, lastprice is the recently price
            model.href='http://www.google.com/finance?q=' \
               +(stock_id[0]=='0' and 'SHE:' or 'SHA:') \
                + stock_id + '&gl=cn'
            
            for price in priceList:
                current_price = price.price
                #logging.error("doudou:" + current_price+ " tmpIndex:" + str(tmpIndex) + " x:" + \
                #        str(getX(tmpIndex)) + " y:" + str(getY(tmpIndex)))
                model.stock_price_list[getX(tmpIndex)][getY(tmpIndex)] = CellModel( \
                          current_price, \
	                             str(price.date))
                if lastprice:
                    fl, fc = (float(lastprice), float(current_price))
                    nextModel = model.stock_price_list[getX(tmpIndex + 1)][getY(tmpIndex+1)]
                    if fl < fc:
                        nextModel.color="blue"
                        if fc - 0 > 0.00001:
                            nextModel.other="<p><font color='blue'>-" \
                              + str(round(100*(fc - fl)/fc, 2)) \
                              +"%</font></p>"
                    else:
                        if fc - 0 > 0.00001:
                            nextModel.other="<p><font color='red'>+" \
                              + str(round(100*(fl - fc)/fc, 2)) \
                              +"%</font></p>"
                lastprice=current_price
                tmpIndex = tmpIndex - 1
        
        for i in range(1, myutils.PER_PRICE_COUNT):
            colTitles.insert(0, str(i) + " day ago")
        colTitles.append("today")
        return (stockModelList, colTitles)		
	
	
    def getPrefix(self):
	    return "/"
	
    def getFavList(self, username):
		return [s.stock_id for s in favorateStock.getFavStocks(username)]
	
    def get(self):
        isAdmin, username, url, url_linktext = self.getUserInfo()
        page = 0;
        pageStr = self.request.get('page')
        if pageStr:
	        page = int(pageStr)
        q = self.request.get('q')
        content = cacheMgr.getPageContent(page, isAdmin, self.getPrefix())
        if content and not q:
	        #not search and get cache, then return the cache
		    self.response.out.write(content)
		    return
		
        stocks = self.getData(username)
        page, light_stock_id, start, end, hasPre, hasNext, nextHref, preHref, totalCount = \
                         self.getPageInfo(stocks, page, q, self.getPrefix())
        stockModelList, colTitles=self.getContent(stocks, start, end, light_stock_id, username)
        pageNoList=[]
        pageNum = (totalCount+myutils.PER_PAGE_COUNT-1)/myutils.PER_PAGE_COUNT
        for i in range(0, pageNum):
            pageNoList.append((i, i+1, page == i))
        template_values = {'username' : username, 
                            'stocks': stockModelList, 
                            'isAdmin' : isAdmin, 
                            'columnCount' : myutils.PER_PRICE_COUNT, 
                            'perPriceLines' : myutils.PRICE_LINES,
                            'columnTitles' : colTitles, 
                            'url' : url, 
					        'url_linktext' : url_linktext,
					        'hasNext' : hasNext,
					        'hasPre' : hasPre,
					        'nextHref' : nextHref,
					        'preHref' : preHref,
					        'pageNoList': pageNoList,
					        'prefix' : self.getPrefix(),
					        'normalPage' : self.isNormal()}
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        content = template.render(path, template_values)
        cacheMgr.cachePageContent(page, isAdmin, self.getPrefix(), content)
        self.response.out.write(content)
    
    def post(self):
	    self.get()
	
    def isNormal(self):
        return True
	

def getX(num):
	return num/myutils.PER_PRICE_COUNT

def getY(num):
	return num%myutils.PER_PRICE_COUNT
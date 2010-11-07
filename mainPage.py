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
from pageStockModel import PageStockModel#
from pageStockModel import CellModel#
import cacheMgr
import urllib

class MainPage(webapp.RequestHandler):
    def get(self):
        logging.debug("query main page")
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
            url_linktext = 'Login'
        logging.debug("user is %s, isAdmin:%s" % (username, str(isAdmin)))
        page = 0;
        pageStr = self.request.get('page')
        if pageStr:
	        page = int(pageStr)
        q = self.request.get('q')
        content = cacheMgr.getPageContent(page, isAdmin)
        if content and not q:
		    self.response.out.write(content)
		    return
        stocks = stock.getStocks()
        totalCount = len(stocks)
        light_stock_id = None
        if page ==0 and q:
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
        if q and not light_stock_id:
			page = 0
        
        start = page * myutils.PER_PAGE_COUNT
        if start >= len(stocks):
	        page = 0
	        start = 0
        end = start + myutils.PER_PAGE_COUNT
        hasNext = True
        hasPre = page > 0
        nextHref = "/?page="+str(page+1)
        preHref = "/?page="+str(page-1)
        if end >= totalCount:
            end = totalCount
            hasNext = False
        logging.debug("get stock from %s to %s" % (str(start), str(end)))
        stockModelList=[]
        colTitles=[]
        for one in stocks[start:end]:
            stock_id = one.stock_id
            priceList = stockPrice.getPriceList(stock_id)
            comment = stockComment.getLastComment(stock_id)
            model = PageStockModel()
            model.stock_name = one.name
            model.stock_id = stock_id
            if comment:
                model.last_comment = (cgi.escape(comment.comment), urllib.quote_plus(str(comment.date)), comment.stock_id)
            if light_stock_id and light_stock_id == stock_id:
				model.high_light = True
			
            stockModelList.append(model)
            tmpIndex = myutils.PER_PRICE_COUNT - 1
            lastprice = None
            #logging.error(one.id)
            model.href='http://www.google.com/finance?q=' \
               +(stock_id[0]=='0' and 'SHE:' or 'SHA:') \
                + stock_id + '&gl=cn'
            for price in priceList:
                current_price = price.price
                model.stock_price_list[tmpIndex] = CellModel( \
                          current_price, \
	                             str(price.date))
                if lastprice:
                    if float(lastprice) < float(current_price):
                        model.stock_price_list[tmpIndex + 1].color="blue"
                lastprice=current_price
                tmpIndex = tmpIndex - 1
        
        for i in range(1, myutils.PER_PRICE_COUNT):
            colTitles.insert(0, str(i) + " day ago")
        colTitles.append("today")
        pageNoList=[]
        pageNum = (totalCount+myutils.PER_PAGE_COUNT-1)/myutils.PER_PAGE_COUNT
        logging.info("pageNum:" + str(pageNum) + ":totalCount:" + str(totalCount) + \
                       ":per:" + str(myutils.PER_PAGE_COUNT))
        for i in range(0, pageNum):
            pageNoList.append((i, i+1, page == i))
        template_values = {'username' : username, \
                            'stocks': stockModelList, \
                            'isAdmin' : isAdmin, \
                            'columnCount' : myutils.PER_PRICE_COUNT, \
                            'columnTitles' : colTitles, \
                            'url' : url, \
					        'url_linktext' : url_linktext,
					        'hasNext' : hasNext,
					        'hasPre' : hasPre,
					        'nextHref' : nextHref,
					        'preHref' : preHref,
					        'pageNoList': pageNoList}
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        content = template.render(path, template_values)
        cacheMgr.cachePageContent(page, isAdmin, content)
        self.response.out.write(content)
    
    def post(self):
	    self.get()

#!/usr/bin/env python
# encoding: utf-8
import logging#
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app#
from mainPage import MainPage#
from updateStock import UpdateStock#
from addNewStock import AddNewStock#
from deleteStock import DeleteStock#
from addStockComment import AddStockComment#
from nextComment import NextComment
from favorateStock import FavStockAction
from mainPageFav import MainPageFav
import security#

#start application
application = webapp.WSGIApplication(
    [('/*$', MainPage), 
     ('/fav/*$', MainPageFav),
     ('/admin/addNewStock', AddNewStock), 
     ('/admin/addStockComment', AddStockComment), 
     ('/admin/updateStockPrice', UpdateStock), 
     ('/admin/user/(add|delete)', security.AuthenUsersAction), 
     ('/admin/deleteStock', DeleteStock),
     ('/admin/nextpage/(\d+)/(.*)$', NextComment),
     ('/admin/fav/(add|delete)/(\d+)$', FavStockAction)],
      debug=True)

def main():
    run_wsgi_app(application)
    logging.info("application started!")

if __name__ == "__main__":
    main()
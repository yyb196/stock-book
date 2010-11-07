#!/usr/bin/env python
# encoding: utf-8
"""
Authen.py

Created by yang frank on 2010-10-10.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.ext import db
import re
import logging
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import myaop
import cacheMgr


def checkUserAuth(username, path=None):
    if users.is_current_user_admin():
        return True
    userList = getUsers()
    username=users.get_current_user().email()
    for user in userList:
        if(user.name == username):
            if path == None:
                return True
            elif path == user.path:
                return True
	
    return False
def getUsers():
	userList = cacheMgr.getUsers()
	logging.debug("get authenUsers from cache is None? %s" % (str(userList==None)))
	if userList:
		return userList
	userList = User.all().fetch(200)
	cacheMgr.cacheUsers(userList)
	return userList
		
class AuthenUsersAction(webapp.RequestHandler):
    @myaop.admin()
    def post(self, operation):
        print operation
        logging.debug("in the user control action")
        if operation == 'add':
			newuser = User(name="x", path="x")
			newuser.name=self.request.get("name")
			newuser.path=self.request.get("path")
			newuser.put()
        else:
			name=self.request.get("name")
			for one in getUsers():
				if(one.name == name):
					one.delete()
        cacheMgr.triggerUserChange()
        self.redirect("/")
			
		
class User(db.Model):
	name = db.StringProperty(required=True)	
	path = db.StringProperty(required=True)

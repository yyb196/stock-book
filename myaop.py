#!/usr/bin/env python
# encoding: utf-8
"""
myaop.py

Created by yang frank on 2010-10-10.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import security
from google.appengine.api import users

def admin(path=None):
    def wrapper(handler_method):
        def check_login(self, *args, **kwargs):
            if security.checkUserAuth(users.get_current_user().nickname(), path):
                return handler_method(self, *args, **kwargs)
            else:
                self.redirect(users.create_login_url("/"))
        return check_login
    return wrapper
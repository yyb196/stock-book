#!/usr/bin/env python
# encoding: utf-8
"""
counter.py

Created by yang frank on 2010-10-17.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db#


class Counter(db.Model):
	id=db.StringProperty(required=True)
	count=db.IntegerProperty(required=True)


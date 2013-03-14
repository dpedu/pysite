#!/usr/bin/env python
import pysite
from pysite import *

class SiteBase(object):
	
	def __init__(self):
		pass
		
	
	def route(self, *args, **kwargs):
		print "SelfRoute has self as %s" % self
		whereTo = args[0]
		def decorator(f):
			print "mapping url %s to method %s" % (whereTo, f)
			self.routes[whereTo] = f
			return f
		return decorator
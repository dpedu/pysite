#!/usr/bin/env python
import cherrypy

class SiteSession:
	# Simple class for manipulating HTTP Session data
	
	def get(self, key, default=None):
		" Return an object from the session "
		return cherrypy.session.get(key, default)
	
	def put(self, key, value):
		" Put and object into the session "
		cherrypy.session[key]=value
	
	def has(self, key):
		" Check if the session has an object identified by key"
		return cherrypy.session.has_key(key)
	
	def delete(self):
		" Clear out the client's session "
		cherrypy.session.delete()

#!/usr/bin/env python
import sys
import cherrypy
import pysite
from pysite import *

import datetime
import time
import os
import yaml

class PySiteRoot(object):
	
	def __init__(self):
		self.config={}
		self.routes={}
		
		self.handler_404 = None
		
		self.conf = yaml.load(file("./config.yml", "r"))["pysite"]
	
	def setup(self):
		
		# Enable import of addons from the mods directory
		sys.path.insert(1, "./mods/")
		
		# Create an instance of the actual website
		self.module = __import__(self.conf["base"]["module"])
		
		# Bind our error handler
		cherrypy.config.update({'error_page.404': self.error_page_404})
		
		# After the website imports what DB stuff it needs, ensure tables are created
		db.Base.metadata.create_all(database.engine)
		
	
	def handler(self, q, **kwargs):
		handlerMethod = None
		
		q = "/"+q
		# Split args seperated by path
		args = q.split("/")
		# Search longest-to-shortest for approprite handler
		# IE, highscores/richest/page/0 then highscores/richest/page then highscores/richest then highscores
		argLen = len(args)
		while True:
			checkSegment='/'.join(args[0:argLen])
			if checkSegment == "":
				checkSegment = "/"
			argsSegment=args[argLen:]
			argLen-=1
			
			if checkSegment in self.routes:
				handlerMethod = self.routes[checkSegment]
				break;
			
			if argLen==0:
				break;
		
		if q == "/" and "<front>" in self.routes:
			handlerMethod = self.routes["<front>"]
		
		if handlerMethod:
			tb = None
			try:
				for line in handlerMethod(checkSegment, argsSegment, **kwargs):
					yield line
			except Exception,e:
				if isinstance(e, cherrypy.HTTPRedirect):
					raise e
				else:
					tb = traceback.format_exc()
			finally:
				if not tb==None:
					errorCode = "h:"+self.md5(str(time.time()))[0:14]
					print "---------- EXCEPTION ID %s ----------" % errorCode
					print tb
					print "---------------------------------------------------"
					raise cherrypy.HTTPError(500, "An internal error prevented this page from loading. Please contact an administrator with the error code: %s" % errorCode)
		else:
			self.HTTPError(404)
	handler.exposed= True
	
	def addUrl(self, path, method):
		self.routes[path] = method
	
	def index(self):
		" Display this if the user didn't set up .htaccess correctly "
		yield "Welcome to pysite! You have not configured the required URL Rewrite."
	index.exposed = True
	
	def error_page_404(self, status, message, traceback, version):
		" Default 404 handler "
		if self.handler_404:
			content = self.handler_404(error={"status":status, "message":message, "traceback":traceback, "version":version})
			#print "%s bytes from error handler" % str(len(content))
			return str(content)
		else:
			return "404 - Page or Error Handler Not Found."
	
	def error404Handler(self, method):
		" 404 Handler Binder "
		self.handler_404 = method
	
	def HTTPError(self, status=500, message=None):
		" Throw arbitrary http errors "
		raise cherrypy.HTTPError(status, message)
	
	def redirect(self, path, httpmethod=302):
		" HTTP Redirect. Defaults to 302 FOUND, Also try 301 MOVED PERMANENTLY "
		raise cherrypy.HTTPRedirect(path, httpmethod)
	
	def quickrender(self, templateFilePath, vars, doTime=True):
		" Simply return a rendered template "
		if doTime and "_timestart" in vars:
			vars['_timeend'] = time.time()
			vars['_rendertime'] = round( (vars['_timeend']-vars['_timestart'])*1000 , 2)
			loads = os.getloadavg()
			vars['_sysload'] = "%s %s %s" % (round(loads[0], 2), round(loads[1], 2), round(loads[2], 2))
		tb = None
		try:
			template = env.get_template(templateFilePath)
			return template.render(vars)
		except Exception,e:
			tb = traceback.format_exc()
		finally:
			if not tb==None:
				errorCode = "q:"+self.md5(str(time.time()))[0:14]
				print "---------- EXCEPTION ID %s ----------" % errorCode
				print tb
				print "---------------------------------------------------"
				raise cherrypy.HTTPError(500, "An internal error prevented this page from loading. Please contact an administrator with the error code: %s" % errorCode)
				return "Error rendering template"
	
	def log(self, section, message):
		print "%s [%s] %s" % (datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), section.upper(), message)
	

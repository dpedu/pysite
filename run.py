#!/usr/bin/env python

# Clear out old sessions BEFORE importing cherry
import os
for f in os.listdir("sessions/"):
	if "lock" in f:
		os.remove("sessions/%s" % f)

import sys
import cherrypy
import yaml
from pysite import pysite

if __name__ == '__main__' or 'uwsgi' in __name__:
	
	conf = yaml.load(file("./config.yml", "r"))["pysite"]
	
	appconf = {
		'/': {
			'tools.proxy.on':True,
			'tools.proxy.base': conf["base"]["url"],
			'tools.sessions.on':True,
			'tools.sessions.storage_type':'file',
			'tools.sessions.storage_path':conf["base"]["basedir"]+'/sessions/',
			'tools.sessions.timeout':525600,
			'request.show_tracebacks': True
		},
		'/media': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': conf["base"]["basedir"]+"/static/"
		}
	}
	
	cherrypy.config.update({
		'server.socket_port':8087,
		'server.thread_pool':1,
		'server.socket_host': '0.0.0.0',
		'sessionFilter.on':True,
		'server.show.tracebacks': True
	})
	
	cherrypy.server.socket_timeout = 5
	
	application = None
	
	print( "Ready to start application" )
	
	if(len(sys.argv)>1 and sys.argv[1]=="test"):
		application = cherrypy.quickstart(pysite, '/app/', appconf)
	else:
		sys.stdout = sys.stderr
		cherrypy.config.update({'environment': 'embedded'})
		application = cherrypy.tree.mount(pysite, "/app/", appconf)
	

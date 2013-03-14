#!/usr/bin/env python

from website import *

from sqlalchemy.orm import aliased
from sqlalchemy import desc,or_,and_,distinct,func

class Main(object):
	
	def __init__(self):
		pass
	
	def cron(self, url, urlargs, **args):
		pass
	
	def index(self, url, urlargs, **args):
		" Index page handler. "
		vars = gatherTemplateVars(url)
		vars["title"]="Page Title"
		s=Session()
		vars["samples"]=s.query(db.Sample).filter(db.Sample.ID==14).order_by(desc(db.Sample.Date)).limit(5).all()
		yield pysite.quickrender('mytemplate.htm', vars)
		s.close()
	
	def handleError(self, error):
		vars = gatherTemplateVars()
		vars["title"]="Error %s" % error["status"]
		vars["pagetitle"]="Error %s" % error["status"]
		vars["message"]=error["message"]
		vars["code"]=error["status"]
		return pysite.quickrender('errors/404.htm', vars)


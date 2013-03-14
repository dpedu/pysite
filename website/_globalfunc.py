#!/usr/bin/env python
from website import db
from pysite import env,Session,pysite,SiteSession
from time import time,mktime

def gatherTemplateVars(activePath=None, options=[]):
	tvars = {}
	tvars['_timestart'] = time()
	tvars['_pid'] = os.getpid()
	
	tvars['titlesuffix'] = " | Global Title Suffix"
	tvars['css'] = [
		{"src":"/libs/reset/reset.css"},
		{"src":"/libs/jquery-ui-bootstrap/css/custom-theme/jquery-ui-1.8.16.custom.css"},
		{"src":"/libs/jquery-ui-bootstrap/bootstrap/bootstrap.css"},
		{"type":"text/css", "rel":"stylesheet/less", "src":"/media/css/styles.less"}
	]
	tvars['js'] = [
		'/libs/lesscss/less-1.3.1.min.js',
		'/libs/jquery/jquery-1.8.3.min.js',
		'/libs/jquery-ui-1.9.2.custom/js/jquery-ui-1.9.2.custom.min.js',
		'/media/js/script.js',
	]
	
	if "admin" in options:
		tvars["css"].append({"type":"text/css", "rel":"stylesheet/less", "src":"/media/css/admin.less"})
		tvars["js"].append('/media/js/admin.js')
	
	return tvars

# Useful methods 
def validEmail(email):
	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return True
	return False 

def hashStr(text):
	" Returns the sha256 hash of a string (for passwords)"
	h = hashlib.sha256()
	h.update(text)
	return h.hexdigest()

def error404(vars):
	vars["title"]="Error"
	vars["pagetitle"]="Error"
	template = env.get_template('errors/404.htm')
	return template.render(**dict(vars.items()))

#### JINJA FILTERS
def datetimeformat(value, format=r'%b %d, %I:%M %p'):
	" Print a datetime object in a nice format "
	return value.strftime(format)
env.filters['datetimeformat'] = datetimeformat

def timeAgoLimit(date, format="%b %d, %I:%M %p", limit=604800):
	" Datetime to time ago from now with a max limit, at which point it falls back to a set format "
	now = int(time())
	duration = time() - mktime(date.timetuple())
	if duration > limit:
		" Older than a week by default "
		return datetimeformat(date, format)
	else:
		return timeago(date)
env.filters['timeAgoLimit'] = timeAgoLimit

def timeago(date):
	" Datetime to vague time ago string "
	now = int(time())
	duration = time() - mktime(date.timetuple())
	if duration < 1:
		return "Just now"
	elif duration < 60:
		return "%s second%s ago" % (int(duration), 's' if int(duration)>1 else '')
	elif duration < 60*60:
		return "%s minute%s ago" % (int(duration/60), 's' if int(duration/60)>1 else '')
	elif duration < 60*60*24:
		return "%s hour%s ago" % (int(duration/60/60), 's' if int(duration/60/60)>1 else '')
	else:
		return "%s day%s ago" % (int(duration/60/60/24), 's' if int(duration/60/60/24)>1 else '')
env.filters['timeago'] = timeago

def timestampToDate(stamp):
	" Convert a unix timestamp to a datetime object "
	return datetime.fromtimestamp(stamp)
env.filters['timestampToDate'] = timestampToDate

def strip(content, remove):
	" Return the input string with remove removed "
	return content.replace(remove, "")
env.filters['strip'] = strip

def slug(content, whitelist="abcdefghijklmnopqrstuvwxyz-_", replace=[(' ', '-')]):
	" Converts a string to a url-friendly format "
	content = content.lower()
	if content == "":
		return "-"
	for set in replace:
		content=content.replace(set[0], set[1])
	output = ""
	for i in range(0, len(content)):
		l = content[i:i+1]
		if l in whitelist:
			output+=l
	if content == "":
		return "-"
	return output
env.filters['slug'] = slug

def escape(content):
	" HTML escape text "
	return content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;")
env.filters['escape'] = escape

def numberFormat(num):
	" Print a number with comma-separation "
	return format(num, ",d")
env.filters['numberFormat'] = numberFormat

def capital(string):
	" Capitalize the first letter of a string, and lowercase the rest "
	if len(string)<=1:
		string.capitalize()
	else:
		return string[0].capitalize()+string[1:]
env.filters['capital'] = capital

def money(value):
	" Displays a number as money "
	locale.setlocale( locale.LC_ALL, '' )
	return locale.currency( float(value), grouping=True )
env.filters['money'] = money

def htmlEncode(s):
	" Encode unicode to html escaped characters "
	return s.encode('ascii', 'xmlcharrefreplace')
	

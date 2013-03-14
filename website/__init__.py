#!/usr/bin/env python

# Import needed objects from pysite
from pysite import pysite          # Root pysite object
from pysite import env             # Templating environment
from pysite import Session         # Database session
from pysite import SiteSession     # HTTP Session manager

from jinja2 import escape          # Commonly used for escaping in HTML

from _globalfunc import *          # Global functions

from website import db             # Our database
from website import main           # A class containing methods the website uses

# Instantiate a website class
root = main.Main()

# Bind our error handler
pysite.error404Handler(root.handleError);

# Bind objects to methods
pysite.addUrl("<front>", root.index)
pysite.addUrl("/cron", root.cron)

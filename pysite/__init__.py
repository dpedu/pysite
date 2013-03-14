#!/usr/bin/env python

from database import Session, env
from pysitesession import *
from pysiteroot import PySiteRoot
from sitebase import SiteBase
import sqlalchemy

SiteSession = SiteSession()
pysite = PySiteRoot()
pysite.setup()

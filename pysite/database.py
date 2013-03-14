#!/usr/bin/env python

from pysite import db
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from jinja2 import Environment, FileSystemLoader
import yaml

# Load config file (Contains database info)
conf = yaml.load(file("./config.yml", "r"))["pysite"]

# Connect to MySQL
engine = sqlalchemy.create_engine(conf["database"]["uri"])
Session = sessionmaker(bind=engine)

# Set up the Jinja environment
env = Environment(loader=FileSystemLoader(conf["base"]["templatedir"]))

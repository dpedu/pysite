#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from pysite.db import Base

from website import Session

class Sample(Base):
	__tablename__ = 'samples'
	
	ID = Column(Integer(), primary_key=True, autoincrement=False)
	UserID = Column(Integer())
	Seen = Column(Boolean())
	Type = Column(Enum('death','res','redeem','donation','thread_reply','thread_comment'))
	ItemID = Column(Integer())
	TransactionID = Column(String(50))
	Date = Column(DateTime())
	
	def __init__(self, UserID, Seen, Type, ItemID, TransactionID, Date):
		self.UserID = UserID
		self.Seen = Seen
		self.Type = Type
		self.ItemID = ItemID
		self.TransactionID = TransactionID
		self.Date = Date
	def toDict(self):
		from dbclass import DBClass
	

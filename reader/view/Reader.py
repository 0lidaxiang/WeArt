#!/usr/bin/python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

class Reader:
	def __init__(self):
		self.id = None
		self.name = None
		self.status = None

	def getId(self, ):
		pass

	def setId(self, id):
		pass

	def getName(self, ):
		pass

	def setName(self, name):
		pass

	def getStatus(self, ):
		pass

	def setStatus(self, status):
		pass

	def lockAccount(self, id):
		pass

	def unlockAccount(self, id):
		pass

	def listInfo(self, pageNum):
		pass

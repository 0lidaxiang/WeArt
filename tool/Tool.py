#!/usr/bin/python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class Tool(View):
	def __init__(self):
		self.template_name = 'register.html'

	# def createId(self, number, category):
	# 	return HttpResponse('result')
	#
	# def registerReader(self, userName, passwd, category):
	# 	return HttpResponse('result')
	#
	#
	# def logout(self, idUser, category):
	# 	pass
	#
	# def login(self, request,*args, **kwargs):
	#     context	= {}
	#     context['athlete_list'] = [{'val':1111},{'val':2222},{'val':333}]
	#     return render(request, self.template_name, context)
	# def register(self,request):
	#     context	= {}
	#     context['homepage'] = 'WeArt'
	#     context['athlete_list'] = [{'val':1111},{'val':2222},{'val':333}]
	#     return render(request, self.template_name, context)

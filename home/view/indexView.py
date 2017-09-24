#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import sys
# import json
# from django.http import JsonResponse
# from book.models import book

from django.shortcuts import render

def index(request):
    context	= {}
    return render(request, 'home/index.html', context)

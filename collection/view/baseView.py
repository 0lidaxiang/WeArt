#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
# from collection.models import collection

def gotoPages(request, pageName):
    if "readerId" not in request.session:
        return 'reader/login.html'
    else:
        return 'collection/' + pageName + '.html'

def addCollectionInter(request):
    print request.GET['idBook']
    return render(request,  gotoPages(request, "addCollectionInter"), {"idBook" : request.GET['idBook']})

#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from author.models import author

def gotoAuthorPages(request, pageName):
    if "readerId" not in request.session:
        return 'reader/login.html'
    if request.session["authorStatus"] == "active":
        return 'author/' + pageName + '.html'
    else:
        return 'author/authorStatus.html'

def getUserName(request):
    if "readerId" not in request.session:
        return 'reader/login.html'
    return request.session["userName"]

def authorStatus(request):
    return render(request,  gotoAuthorPages(request, "authorStatus"), {"userName" : getUserName(request)})

def artsManage(request):
    return render(request,  gotoAuthorPages(request, "artsManage"), {"userName" : getUserName(request)})

def createNewBook(request):
    return render(request,  gotoAuthorPages(request, "createNewBook"), {"userName" : getUserName(request)})

def createNewChapter(request):
    return render(request,  gotoAuthorPages(request, "createNewChapter"), {"userName" : getUserName(request)})

def createNewContent(request):
    return render(request,  gotoAuthorPages(request, "createNewContent"), {"userName" : getUserName(request)})

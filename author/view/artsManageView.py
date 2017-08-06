#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from author.models import author

def authorStatus(request):
    if "readerId" in request.session:
        return render(request, 'author/authorStatus.html')
    else:
        return render(request, 'reader/login.html')

def gotoAuthorPages(request, pageName):
    if "readerId" in request.session:
        if request.session["authorStatus"] == "active":
            return 'author/' + pageName + '.html'
        elif request.session["authorStatus"] == "inactive":
            return 'author/authorStatus.html'
        else:
            return 'reader/login.html'
    else:
        return 'reader/login.html'

def artsManage(request):
    return render(request,  gotoAuthorPages(request, "artsManage"))

def createNewBook(request):
    return render(request,  gotoAuthorPages(request, "createNewBook"))

def createNewChapter(request):
    return render(request,  gotoAuthorPages(request, "createNewChapter"))

def createNewContent(request):
    return render(request,  gotoAuthorPages(request, "createNewContent"))

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

def authorStatus(request):
    return render(request,  gotoAuthorPages(request, "authorStatus"))

def artsManage(request):
    return render(request,  gotoAuthorPages(request, "artsManage"))

def createNewBook(request):
    return render(request,  gotoAuthorPages(request, "createNewBook"))

def createNewChapter(request):
    return render(request,  gotoAuthorPages(request, "createNewChapter"))

def createNewContent(request):
    return render(request,  gotoAuthorPages(request, "createNewContent"))

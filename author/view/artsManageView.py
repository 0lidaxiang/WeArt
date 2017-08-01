#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from author.models import author

def artsManage(request):
    if "readerId" in request.session:
        return render(request, 'author/artsManage.html')
    else:
        return render(request, 'reader/login.html')

def createNewBook(request):
    if "readerId" in request.session:
        return render(request, 'author/createNewBook.html')
    else:
        return render(request, 'reader/login.html')

def createNewChapter(request):
    if "readerId" in request.session:
        return render(request, 'author/createNewChapter.html')
    else:
        return render(request, 'reader/login.html')

def createNewContent(request):
    if "readerId" in request.session:
        return render(request, 'author/createNewContent.html')
    else:
        return render(request, 'reader/login.html')

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from book.models import book
# from django.views.decorators import csrf

import paramiko
import sys
import json
import os
import datetime
import subprocess

def chapterContent(request):
    context = {}
    # get the book id of user input if it is not null
    if 'idBook' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The idBook variable is not in request.GET."
        return JsonResponse(context)
    inputIdBook = request.GET['idBook']

    # get the book name of user input if it is not null
    if 'bookName' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The bookName variable is not in request.GET."
        return JsonResponse(context)
    bookName = request.GET['bookName']

    # get the chapter order of user input if it is not null
    if 'chapterOrder' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The chapterOrder variable is not in request.GET."
        return JsonResponse(context)
    chapterOrder = request.GET['chapterOrder']

    # get the chapter name of user input if it is not null
    if 'chapterName' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The chapterName variable is not in request.GET."
        return JsonResponse(context)
    chapterName = request.GET['chapterName']

    return render(request, 'content/chapterContent.html', context={'idBook': inputIdBook,'chapterOrder': chapterOrder, "chapterName":chapterName, "bookName":bookName})


def readerGetContent(request):
    context = {}
    idBook = request.GET['idBook'];
    chapterOrder = request.GET['chapterOrder'];

    locationBook = ""
    res, statusNumber, mes = book.getValue(idBook, "location")
    if not res:
        context['status'] = "fail"
        context['message'] = str(statusNumber) + " 錯誤： " + mes
        return JsonResponse(context)
    locationBook = mes

    cmd1 = "cd " + locationBook + "/" + idBook
    cmd2= ";cat " + idBook + "_" + chapterOrder + ".txt"
    cmd = cmd1 + cmd2
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    content = list(p.stdout.readlines())
    contentList = []
    for v in content:
        contentList.append(v)

    context["status"] = "success"
    context["message"] = contentList

    return JsonResponse(context)
    # return HttpResponse(json.dumps(contentList), content_type="application/json")

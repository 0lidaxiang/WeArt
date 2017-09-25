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

def authorGetContent(request):
    userInputBookName = request.POST['bookName'];
    chapterOrder = request.POST['chapterOrder'];
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    if request.session["authorStatus"] != "active":
        return 'author/authorStatus.html'

    idReader = request.session['readerId']

    idBook = ""
    res, statusNumber, mes = book.getIdByNameAndAuthor(userInputBookName, idReader)
    if res:
        idBook = mes

    locationBook = ""
    res, statusNumber, mes = book.getValue(idBook, "location")
    if res:
        locationBook = mes

    cmd1 = "cd " + locationBook + "/" + idBook
    cmd2= ";cat " + idBook + "_" + chapterOrder + ".txt"
    cmd = cmd1 + cmd2
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    content = list(p.stdout.readlines())
    contentList = []
    for v in content:
        contentList.append(v)

    return HttpResponse(json.dumps(contentList), content_type="application/json")

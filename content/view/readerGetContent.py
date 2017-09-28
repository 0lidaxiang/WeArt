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
import re

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

def showHistory(request):
        context = {}

        reload(sys)
        sys.setdefaultencoding('utf8')

        context["status"] = "success"
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
        # cmd2= ";cat " + idBook + "_" + chapterOrder + ".txt"
        cmd2= ";git log"
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        logs = list(p.stdout.readlines())



        authorIds = []
        for log in logs:
            if log.startswith('Author: ') :
                tempAuthorId = str(re.findall(r"<(.+)@", log.lstrip('Author: '))[0] )
                if tempAuthorId not in authorIds:
                    authorIds.append(tempAuthorId)

        newLogs = [{}]
        i = 0
        lengthLogs =  len(logs)

        tempNewLog = {"authorId" : "", "commitHead" : "", "date" : "","content" : ""}
        for tempL in logs:

            if  i % 6 == 0 and tempL.startswith('commit '):
                tempNewLog["commitHead"] = tempL.lstrip('commit ').rstrip("\n")
            elif  i % 6 == 1 and tempL.startswith('Author: '):
                tempNewLog["authorId"] = str(re.findall(r"<(.+)@", tempL.lstrip('Author: '))[0] )

            elif  i % 6 == 2  and tempL.startswith('Date: '):
                tempNewLog["date"] = tempL.lstrip('Date: ').rstrip("\n")

            elif  i % 6 == 4 and tempL.startswith(' '):
                tempNewLog["content"] = tempL.lstrip(' ').rstrip("\n")

            if  i % 6 == 5 or i == (lengthLogs -1):
                newLogs.append(dict(tempNewLog))
            i = i + 1

        newLogs.pop(0)

        # print "\n\n--------------newLogs ------------------"
        # for value in newLogs:
        #     print value
        # print "--------------------------newLogs------------------ \n\n"

        authorsAndLogs = []
        for newLog in newLogs:
            authorAndLog =  {"author" : "", "logList" : [], "contenthistory1" : []}
            authorAndLog['author'] = newLog["authorId"]

            # for logV in authorAndLog["logList"]:
            cmd1 = "cd " + locationBook + "/" + idBook
            # cmd2= ";cat " + idBook + "_" + chapterOrder + ".txt"
            cmd2= ";git show " + newLog["commitHead"]
            cmd = cmd1 + cmd2
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            lp = list(p.stdout.readlines())

            flag = False
            for v in lp:
                if v.startswith('@@'):
                    flag = True
                    continue
                if flag == True and v.startswith("+") == True:
                    authorAndLog['contenthistory1'].append(v.lstrip('+'))
                if flag == True and v.startswith("-") == True:
                    authorAndLog['contenthistory1'].remove(v.lstrip('-'))
            authorsAndLogs.append(authorAndLog)

        context['history'] = authorsAndLogs

        # find all log keys of this book

        # return render(request, 'result.html', context)
        return JsonResponse(context)

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

        # print "-------------- authorIds ------------------"
        # for au in authorIds:
        #     print au
        # print "################# authorIds #################"
        # print "\n\n\n"

        authorsAndLogs = []
        for authorId in authorIds:
            authorAndLog =  {"author" : "", "logList" : [], "contenthistory1" : []}
            # authorId = "40f98a05660bf871802e"
            authorAndLog['author'] = authorId

            is_author = False
            logList = []
            for l in logs:
                # print l.lstrip('commit ').rstrip("\n")
                is_author = False
                if l.startswith('commit') :
                    is_author = True

                if (l.find(authorId) > -1):
                    # is_author = False
                    # authorAndLog['logList'].append(l.lstrip('commit').rstrip("\n") )
                    logList.append(l.lstrip('commit').rstrip("\n") )
            authorAndLog['logList'] = logList

            print "author " + authorId + " 's logList： "
            print authorAndLog['logList']

            # contenthistory1 = []
            # authorAndLog["logList"].reverse()
            for logV in authorAndLog["logList"]:
                cmd1 = "cd " + locationBook + "/" + idBook
                # cmd2= ";cat " + idBook + "_" + chapterOrder + ".txt"
                cmd2= ";git show " + logV
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


        print " \n authorsAndLogs:\n\n"
        # print authorsAndLogs
        for value in authorsAndLogs:
            print value["author"]
            print value["logList"]
            # print value["contenthistory1"]

        # print type(authorsAndLogs[0]["contenthistory1"])
        context['history'] = authorsAndLogs[1]["contenthistory1"]






        # find all log keys of this book
        # contentLog = []
        # # is_author = False
        # for v in logs:
        #     # if v.find(request.session['readerId']) > -1 :
        #         # is_author = True
        #     # if is_author and v.startswith('commit'):
        #     if v.startswith('commit'):
        #         contentLog.append(v.lstrip('commit') )
        # context['logs'] = contentLog
        #
        # contenthistory = []
        # contentLog.reverse()
        # for logV in contentLog:
        #     cmd1 = "cd " + locationBook + "/" + idBook
        #     # cmd2= ";cat " + idBook + "_" + chapterOrder + ".txt"
        #     cmd2= ";git show " + logV
        #     cmd = cmd1 + cmd2
        #     p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        #     lp = list(p.stdout.readlines())
        #
        #     flag = False
        #     for v in lp:
        #         if v.startswith('@@'):
        #             flag = True
        #             continue
        #         if flag == True and v.startswith("+") == True:
        #             contenthistory.append(v.lstrip('+'))
        #         if flag == True and v.startswith("-") == True:
        #             contenthistory.remove(v.lstrip('-'))
        # context['history'] = contenthistory
        # print "contenthistory::"
        # print contenthistory

        # return render(request, 'result.html', context)
        return JsonResponse(context)

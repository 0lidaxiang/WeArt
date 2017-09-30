#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from book.models import book
from chapter.models import chapter
from version.models import version

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

        # step1: get version and votes info of every author from databases
        idAuthorsAndVotes = []
        res, statusNumber, mes  = chapter.getValue(idBook ,"id")
        idChapterArg = mes

        if res:
            res,statusNumber,ver = version.getVersionsByIdChapter(idChapterArg)
            for v in ver:
                idAuthorAndVote = {"vote": 0, "score": 0, "idAuthor": ""}
                idAuthorAndVote["vote"] = int(v.vote)
                idAuthorAndVote["score"] = int(v.score)
                idAuthorAndVote["idAuthor"] = v.idAuthor_id
                idAuthorsAndVotes.append(idAuthorAndVote)
        idAuthorsAndVotes.sort(reverse = True, key=lambda x:(x['vote'],x['score']))
        # print idAuthorsAndVotes[0]["idAuthor"]
        # context['idAuthorsAndVotes'] = idAuthorsAndVotes

        # step2: get git-logs of this book
        cmd1 = "cd " + locationBook + "/" + idBook
        cmd2= ";git log"
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        logs = list(p.stdout.readlines())


        # step3： re-strcut the git-logs
        newLogs = [{}]
        i = 0
        lengthLogs =  len(logs)
        tempNewLog = {"authorId" : "", "commitHead" : "", "date" : "","content" : ""}
        for tempL in logs:

            if  i % 6 == 0 and tempL.startswith('commit '):
                tempNewLog["commitHead"] = tempL.lstrip('commit ').rstrip("\n")
            elif  i % 6 == 1 and tempL.startswith('Author: '):
                tempNewLog["authorId"] = str(re.findall(r"<(.+)@", tempL.lstrip('Author: '))[0] )
                for idAuthorAndVote in idAuthorsAndVotes:
                    if idAuthorAndVote["idAuthor"] == tempNewLog["authorId"]:
                        tempNewLog["vote"] = idAuthorAndVote["vote"]
                        break

            elif  i % 6 == 2  and tempL.startswith('Date: '):
                tempNewLog["date"] = tempL.lstrip('Date: ').rstrip("\n")

            elif  i % 6 == 4 and tempL.startswith(' '):
                tempNewLog["content"] = tempL.lstrip(' ').rstrip("\n")

            if  i % 6 == 5 or i == (lengthLogs -1):
                newLogs.append(dict(tempNewLog))
            i = i + 1
        newLogs.pop(0)

        # step4: cat the chapter file content by commit log
        historys = []
        for newLog in newLogs:
            authorAndLog =  {"author" : "", "logList" : [], "contenthistory1" : []}
            authorAndLog['author'] = newLog["authorId"]
            authorAndLog['logList'] = newLog["content"]
            authorAndLog['vote'] = newLog["vote"]

            cmd1 = "cd " + locationBook + "/" + idBook
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
                # if flag == True and v.startswith("-") == True:
                    # authorAndLog['contenthistory1'].remove(v.lstrip('-'))
            historys.append(authorAndLog)

        # print "\n\n--------------historys ------------------"
        # print historys
        historys.sort(reverse = True, key=lambda x:(x['vote']))
        # for v in historys:
            # print v
        # print "--------------------------historys------------------ \n\n"

        # step5: re-strcut the history file content classied by author ，sorted by vote
        newHistory = {"vote": 0, "idAuthor": "", "logList": "", "newestContent": ""}

        context['history'] = historys
        return JsonResponse(context)

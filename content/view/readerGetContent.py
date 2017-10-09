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
        reload(sys)
        sys.setdefaultencoding('utf8')

        idBook = request.GET['idBook'];
        chapterOrder = request.GET['chapterOrder'];

        context = {}
        locationBook = ""
        res, statusNumber, mes = book.getValue(idBook, "location")
        if not res:
            context['status'] = "fail"
            context['message'] = str(statusNumber) + " 錯誤： " + mes
            return JsonResponse(context)
        locationBook = mes

        # authorList: get authors list, just for html to list
        cmd1 = "cd " + locationBook + "/" + idBook
        cmd2= ";git log --all --format='%aN' | sort -u"
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        authors = p.stdout.readlines()
        context['authorList'] = authors

        # lastest content of the author which you want to search
        idAuthorToSearch = ""
        if "idAuthor" in request.GET :
            idAuthorToSearch = request.GET["idAuthor"]
        else:
            # step1: get version and votes info of every author from databases
            idAuthorsAndVotes = []
            res, statusNumber, mes  = chapter.getValue(idBook ,"id")
            idChapterArg = mes
            if res:
                res,statusNumber,ver = version.getVersionsByIdChapter(idChapterArg)
                # print type( list(ver) )
                # print ver
                # print "\n\n"
                for v in ver:
                    idAuthorAndVote = {"vote": 0, "score": 0, "idAuthor": ""}
                    idAuthorAndVote["vote"] = int(v.vote)
                    idAuthorAndVote["score"] = int(v.score)
                    idAuthorAndVote["idAuthor"] = v.idAuthor_id
                    idAuthorsAndVotes.append(idAuthorAndVote)
            idAuthorsAndVotes.sort(reverse = True, key=lambda x:(x['vote'],x['score']))
            idAuthorToSearch = idAuthorsAndVotes[0]["idAuthor"]

        # step2: lastest content of the author which you want to search
        status,mes = getLastestContent(idBook, chapterOrder, idAuthorToSearch, locationBook)
        if status:
            context["status"] = "success"
        else:
            context["status"] = "fail"
        context['content'] = mes
        return JsonResponse(context)

def getLastestContent(idBook, chapterOrder, idAuthorToSearch, locationBook):
    try:
        # get latest log sha1Vals of the author which you want to search
        cmd1 = "cd " + locationBook + "/" + idBook
        cmd2= ";git log --date=format:'%Y-%m-%d %H:%M:%S' --author " + idAuthorToSearch + " -1  --pretty=format:'%H'"
            # + " -1  --pretty=format:'%H  %an  %ad  %s'"
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        sha1Vals = list(p.stdout.readlines())

        # get content of every latest log sha1Vals for the file which you want to search
        sha1ValToSearch = sha1Vals[0]
        cmd1 = "cd " + locationBook + "/" + idBook
        cmd2= ";git show " + sha1ValToSearch + ":" + idBook + "_" + chapterOrder + ".txt"
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        content = list(p.stdout.readlines())
        return True, content
    except Exception as e:
        return False, str(e)

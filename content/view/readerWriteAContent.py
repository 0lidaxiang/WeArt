#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
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

def readerCreateNewContent(request):
    if "readerId" not in request.session:
        return HttpResponseRedirect("/reader/login/")

    if "idBook" not in request.GET:
        return render(request, "reader/login.html")

    idBook = request.GET["idBook"]
    return render(request, "content/readerCreateNewContent.html" , {"idBook":idBook})

def readerWriteAContentHtml(request):
    context = {}
    idBook = request.GET["idBook"]

    if "readerId" not in request.session:
        lastUrl = request.GET["lastUrl"]

        context['status'] = "success"
        context['message'] = "/reader/login/?lastUrl=" + "/content/readerCreateNewContent/?idBook=" + idBook
        return JsonResponse(context)
    else:
        readerId = request.session["readerId"]
        reload(sys)
        sys.setdefaultencoding('utf8')

        context['status'] = "success"
        context['message'] = "/content/readerCreateNewContent/?idBook=" + idBook
        return JsonResponse(context)

def readerWriteAContent(request):
        if "readerId" not in request.session:
            return render(request, 'reader/login.html')
        readerId = request.session["readerId"]
        reload(sys)
        sys.setdefaultencoding('utf8')

        context = {}

        # get the new book name of user input if it is not null
        if 'bookName' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The bookName variable is not in request.GET."
            return JsonResponse(context)
        userInputBookName = request.GET['bookName']
        if userInputBookName == "":
            context['status'] = "fail"
            context['message'] = "您還沒有填寫書名稱。請重載後重新嘗試。"
            return JsonResponse(context)

        # get the new chapter name of user input if it is not null
        if 'chapterOrder' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The chapter name variable is not in request.GET."
            return JsonResponse(context)
        userInputChpaterOrder = request.GET['chapterOrder']
        if userInputChpaterOrder == "":
            context['status'] = "fail"
            context['message'] = "您還沒有填寫章節序號。請重載後重新嘗試。"
            return JsonResponse(context)

        # get the new commit content of user input if it is not null
        if 'commitContent' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The commitContent variable is not in request.GET."
            return JsonResponse(context)
        userInputCommitContent = request.GET['commitContent']
        if userInputBookName == "":
            context['status'] = "fail"
            context['message'] = "您還沒有填寫更新摘要名稱。請重載後重新嘗試。"
            return JsonResponse(context)

        # get the new content of user input even if it is null
        if 'content' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The content variable is not in request.GET."
            return JsonResponse(context)
        userInputContent = request.GET['content']

        try:
            # step1: get idBook and check whether a book is exist by bookname

            # step2: get new book name and create file in webServer
            idBook = request.GET["idBook"]
            locationBook = ""
            res, statusNumber, mes = book.getValue(idBook, "location")
            if res:
                locationBook = mes

            myhome_path = locationBook + "/" + idBook

            filePath = myhome_path + "/" + idBook + "_" + str(userInputChpaterOrder) + ".txt"
            f = open(filePath, "w")
            f.write(request.GET['content'] + "\n")
            f.close()

            # step3: modify the git config info to this author
            cmd1 = "cd " + myhome_path
            cmd2 = "; git config --local user.name '" + readerId + "'"
            cmd3 = "; git config --local user.email " + readerId + "@weart.com; "

            cmd = cmd1 + cmd2 + cmd3

            p = subprocess.Popen(cmd, shell=True)
            (stdoutput,erroutput) = p.communicate()

            # step4: git commit to gitServer
            # 新建版本库对象
            repo = Repo(myhome_path)
            # 获取版本库暂存区
            index = repo.index
            # 添加修改文件
            index.add([idBook + "_" + str(userInputChpaterOrder) + ".txt"])
            # 提交修改到本地仓库
            index.commit(userInputCommitContent)
            # 获取远程仓库
            remote = repo.remote()
            origin = repo.remotes.origin
            # 推送本地修改到远程仓库
            origin.push()

            # step5: write data into version table
            res, statusNumber, mes  = chapter.getValue(idBook ,"id")
            idChapter = mes
            if res:
                res, statusNumber, mes = version.add(idChapter, 0, 0, readerId)
                if res:
                    context['status'] = "success"
                    context['message'] = '您已經成功更新 《' + userInputBookName + "》的第 " + userInputChpaterOrder + " 章節內容。"
                    return JsonResponse(context)

            context['status'] = "fail"
            context['message'] = '錯誤： ' + str(statusNumber) + " ， " + mes

        except Exception as e:
            context['status'] = "fail"
            context['message'] = "異常錯誤: " + str(e)

        return JsonResponse(context)

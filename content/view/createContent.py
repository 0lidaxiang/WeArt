#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from book.models import book

import paramiko
import sys
import json
import os
import datetime
import subprocess

def createAContent(request):
    context = {}
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    if request.session["authorStatus"] != "active":
        return render(request, 'author/authorStatus/')

    reload(sys)
    sys.setdefaultencoding('utf8')

    readerId = request.session["readerId"]

    serverHomeDir = "/home/lidaxiang"

    # get the new book name of user input if it is not null
    if 'bookName' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The bookname variable is not in request.GET."
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

    # get the new content of user input if it is not null
    if 'content' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The content variable is not in request.GET."
        return JsonResponse(context)
    userInputContent = request.GET['content']

    try:
        # check whether a book is exist by bookname and idAuthor_id  before writing data into database
        authorId = request.session['authorId']
        res, statusNumber, mes = book.getIdByNameAndAuthor(userInputBookName, authorId)
        if res:
            context = {}
            # get new book name and create respository in remote server
            idBook = mes
            locationBook = ""
            res, statusNumber, mes = book.getValue(idBook, "location")
            if res:
                locationBook = mes
            else:
                pass

            myhome_path = locationBook + "/" + idBook

            filePath = myhome_path + "/" + idBook + "_" + str(userInputChpaterOrder) + ".txt"
            f = open(filePath, "w")
            f.write(request.GET['content'] + "\n")
            f.close()

            cmd1 = "cd " + myhome_path
            cmd2 = "; git config --global user.email user1@gmail.com; git config --global user.name user1"
            cmd = cmd1 + cmd2
            p = subprocess.Popen(cmd, shell=True)
            (stdoutput,erroutput) = p.communicate()

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

            context['status'] = "success"
            context['message'] = '您已經成功更新 《' + userInputBookName + "》的第 " + userInputChpaterOrder + " 章節內容。"
            return JsonResponse(context)

        # this author dont have this book
        if statusNumber == 130004:
            context['status'] = "fail"
            context['message'] = "不存在該本書！請重新輸入其它書名或登錄其它賬號"
        elif statusNumber == 130005:
            context['status'] = "fail"
            context['message'] = "未知服務器錯誤：" + str(statusNumber) + mes
        else:
            context['status'] = "fail"
            context['message'] = "其它服務器錯誤：" + str(statusNumber) + mes

    except Exception as e:
        context['status'] = "fail"
        context['message'] = "異常錯誤: " + str(e)
    return JsonResponse(context)

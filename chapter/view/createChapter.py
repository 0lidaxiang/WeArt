#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from author.models import author
from book.models import book

import paramiko
import sys
import json
import os
import datetime
import subprocess

def createChapter(request):
    context = {}
    if "readerId" in request.session:
        if request.session["authorStatus"] == "active":
            reload(sys)
            sys.setdefaultencoding('utf8')

            readerId = request.session["readerId"]
            # loginId = "lidaxiang"

            # webServerHomeDir = "/home/" + loginId
            webServerHomeDir = "/home"

            # get new book name and create respository in remote server
            request.encoding='utf-8'
            bookName = ""

            try:
                if 'bookName' in request.GET:
                    userInputBookName = request.GET['bookName']

                    if userInputBookName == "":
                        context['status'] = "fail"
                        context['message'] = "您還沒有填寫新書名稱。請重載後重新嘗試。"
                    else:
                        if 'chapterName' in request.GET:
                            userInputChapterName = request.GET['chapterName']

                            if userInputChapterName == "":
                                context['status'] = "fail"
                                context['message'] = "The chapter name is null."
                            else:
                                if 'chapterOrder' in request.GET:
                                    userInputChapterNumber = request.GET['chapterOrder']

                                    if userInputChapterNumber == "":
                                        context['status'] = "fail"
                                        context['message'] = "The chapter number is null."
                                    else:

                                        authorId = request.session['authorId']
                                        bookName = authorId + "_" + userInputBookName

                                        # step1: get operateDir and struct the chapter file name
                                        operateDir = book.getValue(bookName, "location")
                                        chapterFileName = bookName + "_" + userInputChapterNumber
                                        # step2: create a chapter file in webServer
`                                       res, mes = touchChapterFile(operateDir, chapterFileName)
                                        if res:
                                            # step3: git commit this chapter file to gitServer
                                            res, mes = gitCommitChapter(operateDir, chapterFileName, commitContent)
                                            if res:
                                                # step 4: write relative data into database

                                                # bookName_number_chapterName
                                                # now = datetime.datetime.now()
                                                # monthClassedDirName = "/home/" + gitserver_user + "/" + str(now.year) + "/" + str(now.month)
                                                # localMonthClassedDir= webServerHomeDir + "/" + str(now.year) + "/" + str(now.month)
                                            else:
                                                context['status'] = "fail"
                                                context['message'] = mes
                                        else:
                                            context['status'] = "fail"
                                            context['message'] = mes
                        else:
                            context['status'] = "fail"
                            context['message'] = "The chapterName variable is not in request.GET."
                else:
                    context['status'] = "fail"
                    context['message'] = "The bookName variable is not in request.GET."
            except Exception as e:
                        context['status'] = "fail"
                        context['message'] = str(e)
            return JsonResponse(context)
        else:
            return render(request, 'author/authorStatus/')
    else:
        return render(request, 'reader/login.html')

def touchChapterFile(operateDir, fileName):
    try:
        # cmd = "git config --global user.email user1@gmail.com; git config --global user.name user1"
        cmd = "cd " + operateDir + ";touch " + fileName
        p = subprocess.Popen(cmd, shell=True)
        (stdoutput,erroutput) = p.communicate()
        return True,""
    except Exception as e:
        return False,str(e)

def gitCommitChapter(operateDir, fileName, userName, userEmail, commitContent):
    try:
        cmd1 = "cd " + operateDir
        cmd2 = "; git config --local user.email " + userEmail + "; git config --local user.name " + userName
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True)
        (stdoutput,erroutput) = p.communicate()

        # if gi config success
            # repo = Repo(operateDir)
            # # 获取版本库暂存区
            # index = repo.index
            # # 添加修改文件
            # index.add([fileName])
            # # 提交修改到本地仓库
            # index.commit(commitContent)

        return True,""
    except Exception as e:
        return False,str(e)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from book.models import book
from chapter.models import chapter

import paramiko
import sys
import json
import os
import datetime
import subprocess

def createAChapter(request):
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

                                        # get the book id and check whether it exists by bookname and idAuthor_id
                                        res, statusNumber, idBook = book.getIdByNameAndAuthor(userInputBookName, authorId)
                                        if res:
                                            # bookName = authorId + "_" + userInputBookName
                                            # step0: check the book is or not has this chapter
                                            res,statusNumber,mes = chapter.getValue(idBook, "chapterOrder")
                                            if res:
                                                context['status'] = "fail"
                                                context['message'] = "本書已創建該章節！請檢查章節列表後輸入後續章節序號"
                                            else:
                                                if statusNumber == 140003:
                                                    context['status'] = "fail"
                                                    context['message'] = "查詢錯誤，所要查詢的內容不存在！"
                                                elif statusNumber == 140004:
                                                    context['status'] = "success"
                                                    # context['message'] = "本書不存在該章節！"

                                                    # step1: get operateDir and struct the chapter file name
                                                    res,mes = book.getValue(idBook, "location")
                                                    if res:
                                                        operateDir = mes
                                                        chapterFileName = bookName + "_" + userInputChapterNumber
                                                        # step2: create a chapter file in webServer
                                                        res,mes = touchChapterFile(operateDir,chapterFileName)
                                                        if res:
                                                            # step3: git commit this chapter file to gitServer
                                                            res, mes = gitCommitChapter(operateDir, chapterFileName, commitContent)
                                                            if res:
                                                                # step 4: write relative data into database

                                                                # bookName_number_chapterName
                                                                # now = datetime.datetime.now()
                                                                # monthClassedDirName = "/home/" + gitserver_user + "/" + str(now.year) + "/" + str(now.month)
                                                                # localMonthClassedDir= webServerHomeDir + "/" + str(now.year) + "/" + str(now.month)
                                                                pass
                                                            else:
                                                                context['status'] = "fail"
                                                                context['message'] = mes
                                                        else:
                                                            context['status'] = "fail"
                                                            context['message'] = mes
                                                    else:
                                                        context['status'] = "fail"
                                                        context['message'] = mes
                                                else:
                                                    context['status'] = "fail"
                                                    context['message'] = "服務器錯誤：" + statusNumber + mes
                                        else:
                                            context['status'] = "fail"

                                            if statusNumber == 130004:
                                                context['message'] = "不存在該本書！請重新確定您輸入的書名和賬號"
                                            elif statusNumber == 130005:
                                                context['message'] = "服務器錯誤：" + statusNumber + mes
                                            else:
                                                context['message'] = "服務器錯誤：" + statusNumber + mes
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

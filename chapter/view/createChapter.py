#!/usr/bin/python
# -*- coding: utf-8 -*-

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

def createAChapter(request):
    context = {}

    # check this request's account status
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    if request.session["authorStatus"] != "active":
        return render(request, 'author/authorStatus/')

    # dealing with Chinese questions
    reload(sys)
    sys.setdefaultencoding('utf8')

    try:
        # get new book name of user input and check whether it is null
        if 'bookName' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The bookName variable is not in request.GET."
            return JsonResponse(context)
        userInputBookName = request.GET['bookName']

        if userInputBookName == "":
            context['status'] = "fail"
            context['message'] = "您還沒有填寫新書名稱。請重載後重新嘗試。"
            return JsonResponse(context)

        # get the idBook and check whether it exists by bookname and idReader_id
        readerId = request.session['readerId']
        res, statusNumber, idBook = book.getIdByNameAndAuthor(userInputBookName, readerId)
        if not res:
            context['status'] = "fail"
            if statusNumber == 130004:
                context['message'] = "不存在該本書！請重新確定您輸入的書名和賬號"
            elif statusNumber == 130005:
                context['message'] = "服務器錯誤：" + str(statusNumber) + mes
            else:
                context['message'] = "未知服務器錯誤：" + str(statusNumber) + mes
            return JsonResponse(context)

        # get new chapter number of user input and check whether it is null
        if 'chapterOrder' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The chapterOrder variable is not in request.GET."
            return JsonResponse(context)
        userInputChapterNumber = request.GET['chapterOrder']

        if userInputChapterNumber == "":
            context['status'] = "fail"
            context['message'] = "您還沒有填寫章節序號！"
            return JsonResponse(context)

        # get new chapter name of user input and check whether it is null
        if 'chapterName' not in request.GET:
            context['status'] = "fail"
            context['message'] = "The chapterName variable is not in request.GET."
            return JsonResponse(context)
        userInputChapterName = request.GET['chapterName']

        if userInputChapterName == "":
            context['status'] = "fail"
            context['message'] = "您還沒有填寫章節名！"
            return JsonResponse(context)

        # database and file operation start
        # step1: check whether the chapterCount is right.this means whether we can create this chapter
        chapterCount = 10000
        res,statusNumber,mes = book.getValue(idBook, "chapterCount")
        if not res:
            if statusNumber == 130001:
                context['status'] = "fail"
                context['message'] = "查詢條件輸入錯誤！"
            elif statusNumber == 130002:
                # the book is not existing searching according by idBook
                context['status'] = "fail"
                context['message'] = "不存在這本書！請確認輸入後重試！"
            elif statusNumber == 130003:
                context['status'] = "fail"
                context['message'] = "異常錯誤: "+ str(statusNumber) + str(mes)
            else:
                context['status'] = "fail"
                context['message'] = "未知服務器錯誤：" + str(statusNumber) + str(mes)
            return JsonResponse(context)

        # the chapterCount of userInput can not be smaller or larger than (this book's chapter number + 1)
        if int(userInputChapterNumber) != (mes+1):
            context['status'] = "fail"
            context['message'] = "章節序號不正確！請確認後重新填寫章節序號！本書下一章節序號為 " + str(mes+1)
            return JsonResponse(context)

        # step2: struct the chapter file name
        chapterCount = mes
        chapterNowNumber = chapterCount+1
        chapterFileName = idBook + "_" + str(chapterNowNumber) + ".txt"

        # step3: get book's location
        res, statusNumber, mes = book.getValue(idBook, "location")
        if not res:
            if statusNumber == 130001:
                context['status'] = "fail"
                context['message'] = "查詢條件輸入錯誤！"
            elif statusNumber == 130002:
                # the book is not existing searching according by idBook
                context['status'] = "fail"
                context['message'] = "不存在這本書！請確認輸入後重試！"
            elif statusNumber == 130003:
                context['status'] = "fail"
                context['message'] = "異常錯誤: "+ str(statusNumber) + mes
            else:
                context['status'] = "fail"
                context['message'] = "未知服務器錯誤：" + str(statusNumber) + mes
            return JsonResponse(context)
        operateDir = mes + "/" + idBook

        # step4: create a chapter file in webServer
        res,mes = touchChapterFile(operateDir, chapterFileName)
        if not res:
            context['status'] = "fail"
            context['message'] = "3 : Touching chapter file fails." + mes
            return JsonResponse(context)

        # step5: git commit this chapter file to gitServer
        commitContent = "add the chapter " + str(chapterNowNumber)
        res, mes = gitCommitChapter(operateDir, chapterFileName, readerId , readerId + "@weart.com", commitContent)
        if not res:
            context['status'] = "fail"
            context['message'] = "2 : commit failed. " + mes
            return JsonResponse(context)

        # step 7: write data into table book
        res, mes = book.modify(idBook, "chapterCount", chapterNowNumber)
        if not res:
            context['status'] = "fail"
            context['message'] = "0 : " + mes
            return JsonResponse(context)

        # step 8: write data into table chapter
        res, mes = chapter.add(userInputChapterName, chapterFileName, chapterNowNumber, idBook)
        if res:
            idChapter = mes
            res, statusNumber, mes = version.add(idChapter, 0, 0, readerId)
            if res:
                context['status'] = "success"
                context['message'] = '您已經成功更新 《' + userInputBookName + "》的第 " + str(chapterNowNumber) + " 章節內容。"
            else:
                context['status'] = "fail"
                context['message'] = str(statusNumber) + " : " + mes
            return JsonResponse(context)
        else:
            context['status'] = "fail"
            context['message'] = "createAChapter error : " + mes
        # database and file operation end

    except Exception as e:
                context['status'] = "fail"
                context['message'] = "異常錯誤 : " + str(e)
    return JsonResponse(context)

def touchChapterFile(operateDir, fileName):
    try:
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
        repo = Repo(operateDir)
        # 获取版本库暂存区
        index = repo.index
        # 添加修改文件
        index.add([fileName])
        # 提交修改到本地仓库
        index.commit(commitContent)

        return True,""
    except Exception as e:
        return False,str(e)

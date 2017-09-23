#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from author.models import author
from subprocess import Popen, PIPE, check_call
from django.conf import settings
import paramiko
import datetime
import os

def gotoReaderPages(request, pageName):
    # when login, it will check reader's status after readerId
    if "readerId" in request.session:
        return 'reader/' + pageName + '.html'
    else:
        return 'reader/login.html'

def readerIndex(request):
    return render(request,  gotoReaderPages(request, "readerIndex"), {"userName": request.session['userName']})

def booksRecorded(request):
    return render(request,  gotoReaderPages(request, "booksRecorded"), {"userName": request.session['userName']})

def readingHistory(request):
    return render(request,  gotoReaderPages(request, "readingHistory"), {"userName": request.session['userName']})

def readerSetting(request):
    return render(request,  gotoReaderPages(request, "readerSetting"), {"userName": request.session['userName']})

def getEnableAuthorStatus(request):
    try:
        if "readerId" in request.session:
            readerId = request.session["readerId"]

            data = {}
            data['status'] = 'success'
            isAuthor = False
            authorStatus = ""
            if author.isExist(readerId):
                isAuthor = True
                request.session["isAuthor"] = True

                # authorStatus maybe active or inactive or banned
                authorStatus = author.getStatus(readerId)
                if authorStatus:
                    request.session["authorStatus"] = authorStatus
                else:
                    request.session["authorStatus"] = ""
            data["isAuthor"] = isAuthor
            data["authorStatus"] = authorStatus

            return JsonResponse(data)
        else:
            data['status'] = 'fail'
            return render(request, 'reader/login.html')
    except Exception as e:
        data['status'] = 'fail'
        return JsonResponse(data)

def modifyAuthorStatus(request):
    status = ""
    if request.POST:
        status = request.POST['status']

    if "readerId" in request.session:
        data = {}

        try:
            readerId = request.session["readerId"]
            data['status'] = 'success'
            # check thatreader is or is not a author
            if author.isExist(readerId):
                # when reader is a author
                request.session["isAuthor"] = True
                data['isAuthor'] = True

                authorStatus = author.getStatus(readerId)
                # check author status
                if authorStatus == "active":
                    # disable author function when reader is registed and status is "active"
                    # step: modify the value of author's status in database
                    result = author.modifyStatus(readerId, status)
                    if result:
                        request.session["authorStatus"] = status
                        data['authorStatus'] = status #"inactive"
                    else:
                        data['authorStatus'] = request.session["authorStatus"]
                elif authorStatus == "inactive":
                    # modify database
                    if author.modifyStatus(readerId, "active"):
                        data['authorStatus'] = "active"
                        data['message'] = ""
                        request.session["authorStatus"] = "active"
                        request.session["authorId"] = str(author.getId(readerId))
                    else:
                        data['status'] = "fail"
                        data['authorStatus'] = "inactive"
                        data['message'] = "啓用作者功能失敗！請刷新後重新嘗試或聯繫網站管理員！"
                else:
                    data['status'] = "fail"
                    data['authorStatus'] = authorStatus
                    data['message'] = "讀取作者狀態異常!"
                    request.session["authorStatus"] = authorStatus
            else:
                # when reader is not a author
                # step1: add data to table "author" in database
                if  author.addAuthor(readerId):
                    data['status'] = "success"
                    data['isAuthor'] = True
                    data['authorStatus'] = "active"
                    data['message'] = ""

                    request.session["isAuthor"] = True
                    request.session["authorStatus"] = "active"
                else:
                    # This needs to check and delete error data in database.

                    data['status'] = "fail"
                    data['isAuthor'] = False
                    data['authorStatus'] = "inactive"
                    data['message'] = "啓用作者功能失敗！添加資料到數據庫中失敗！請刷新後重新嘗試或聯繫網站管理員！"

                    request.session["isAuthor"] = False
                    request.session["authorStatus"] = "inactive"

        except Exception as e:
            data['status'] = 'fail'
            data['message'] = str(e)
        return JsonResponse(data)
    else:
        return render(request, 'reader/login.html')

def activeAuthorFunction(request,readerId):
    # enable author function when reader is registed and status is "inactive"
    # step1: mkdir in git server
    # statp2: modify the value of author's status in database
    result = author.modifyStatus(readerId, "active")
    if result:
        # return status,authorStatus,message
        return "success","active",mes
    else:
        # return status,authorStatus,message
        return "success","active",mes

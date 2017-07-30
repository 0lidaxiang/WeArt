#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from author.models import author

def readerIndex(request):
    if "readerId" in request.session:
        return render(request, 'reader/readerIndex.html')
    else:
        return render(request, 'reader/login.html')

def booksRecorded(request):
    if "readerId" in request.session:
        return render(request, 'reader/booksRecorded.html')
    else:
        return render(request, 'reader/login.html')

def readingHistory(request):
    if "readerId" in request.session:
        return render(request, 'reader/readingHistory.html')
    else:
        return render(request, 'reader/login.html')

def readerSetting(request):
    if "readerId" in request.session:
        return render(request, 'reader/readerSetting.html')
    else:
        return render(request, 'reader/login.html')

def getEnableAuthorStatus(request):
    try:
        if "readerId" in request.session:
            readerId = request.session["readerId"]

            data = {}
            data['status'] = 'success'
            isAuthor = False
            authorStatus = ""
            if author.isExistIdReader(readerId):
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
        readerId = request.session["readerId"]

        data = {}
        try:
            data['status'] = 'success'
            if author.isExistIdReader(readerId):
                request.session["isAuthor"] = True
                data['isAuthor'] = True

                authorStatus = author.getStatus(readerId)
                if authorStatus == "active" or authorStatus == "inactive":
                    result = author.modifyStatus(readerId, status)
                    if result:
                        request.session["authorStatus"] = status
                        data['authorStatus'] = status
                    else:
                        # request.session["authorStatus"] = "inactive"
                        data['authorStatus'] = request.session["authorStatus"]
                else:
                    request.session["authorStatus"] = authorStatus
                    data['authorStatus'] = authorStatus
            else:
                if  author.addAuthor(readerId):
                    request.session["isAuthor"] = True
                    request.session["authorStatus"] = "active"

                    data['isAuthor'] = True
                    data['authorStatus'] = "active"
                else:
                    request.session["isAuthor"] = False
        except Exception as e:
            data['status'] = 'fail'

        # data['message'] = {"isAuthor" : request.session["isAuthor"]}
        return JsonResponse(data)
    else:
        return render(request, 'reader/login.html')

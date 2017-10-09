#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import json
from django.http import JsonResponse

from django.shortcuts import render
from book.models import book
from chapter.models import chapter

def bookChapter(request):
    context = {}
    # get the book id of user input if it is not null
    if 'idBook' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The idBook variable is not in request.GET."
        return JsonResponse(context)
    inputIdBook = request.GET['idBook']

    # get the book name of user input if it is not null
    # if 'bookName' not in request.GET:
    #     context['status'] = "fail"
    #     context['message'] = "The bookName variable is not in request.GET."
    #     return JsonResponse(context)
    # bookName = request.GET['bookName']
    bookName = ""
    res, status, mes = book.getValue(inputIdBook, "name")
    if res:
        bookName = mes
    else:
        print "getchapter bookChapter error" + str(status)

    return render(request, 'chapter/bookChapter.html', context={'idBook': inputIdBook,'bookName': bookName})

def getChapter(request):
    context = {}
    reload(sys)
    sys.setdefaultencoding('utf8')

    # get the new book name of user input if it is not null
    if 'idBook' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The idBook variable is not in request.GET."
        return JsonResponse(context)
    inputIdBook = request.GET['idBook']

    res, statusNumber, mes = chapter.getAll(inputIdBook)

    if not res:
        context['status'] = "fail"
        context['message'] = "錯誤： " + mes
        return JsonResponse(context)

    context['status'] = "success"

    response_data = []
    for m in mes:
        response_record = {}
        response_record['id'] = m.id
        response_record['name'] = m.name
        response_record['chapterOrder'] = m.chapterOrder
        response_record['idBook_id'] = m.idBook_id
        response_data.append(response_record)

    context["message"] = response_data

    return JsonResponse(context)

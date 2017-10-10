#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
import sys
from book.models import book

def getMyBook(request):
    # dealing with Chinese questions
    reload(sys)
    sys.setdefaultencoding('utf8')

    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idReader = request.session["readerId"]
    context = {}
    try:
        res, status, mes = book.getAllByAuthor(idReader)
        # print res,status, mes
        books = []
        if not res:
            bookTemp = {}
            bookTemp["id"] = 0
            bookTemp["bookName"] = "Server Error"
            bookTemp["chapterCount"] = str(status)
            bookTemp["status"] = str(mes)
            bookTemp["createTime"] = str(mes)
            bookTemp["operation"] = str(mes)
            books.append(bookTemp)
            context['data'] = books
            return JsonResponse(context)

        idx = 0
        for v in mes:
            bookTemp = {}
            bookTemp["id"] = idx
            bookTemp["bookName"] = v.name
            bookTemp["chapterCount"] = v.chapterCount
            bookTemp["status"] = v.status
            bookTemp["createTime"] = v.createTime
            bookTemp["operation"] = "<a href=javascript:deleteBook('" + v.id + "');> delete"  + "</a>"
            books.append(bookTemp)
            idx+=1
        context['data'] = books
        return JsonResponse(context)
    except Exception as e:
        coll = {}
        coll["id"] = 0
        coll["idReader"] = "Server Exception"
        coll["idBook"] = str(130501)
        coll["bookName"] = str(e)
        coll["createTime"] = str(e)
        coll["operation"] = str(e)
        collections.append(coll)
        context['data'] = collections
        return JsonResponse(context)

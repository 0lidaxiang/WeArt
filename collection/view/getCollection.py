#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
import sys
from book.models import book
from collection.models import collection

def getMyCollection(request):
    # dealing with Chinese questions
    reload(sys)
    sys.setdefaultencoding('utf8')

    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idReader = request.session["readerId"]
    context = {}
    try:
        res, status, mes = collection.getAll(idReader)

        collections = []
        if not res:
            coll = {}
            coll["id"] = 0
            coll["idReader"] = "Server Error"
            coll["idBook"] = str(status)
            coll["bookName"] = str(mes)
            coll["createTime"] = str(mes)
            coll["operation"] = str(mes)
            collections.append(coll)
            context['data'] = collections
            return JsonResponse(context)
        idx = 0
        for v in mes:
            coll = {}
            res,status,mes = book.getValue(v.idBook_id, "name")
            if res:
                coll["id"] = idx
                coll["idReader"] = v.idReader_id
                coll["idBook"] = v.idBook_id
                coll["bookName"] = str(mes)
                coll["createTime"] = v.createTime
                coll["operation"] = "<a href=javascript:deleteCollection('" + v.id + "');> delete"  + "</a>"
            collections.append(coll)
            idx+=1

        context['data'] = collections
        return JsonResponse(context)
    except Exception as e:
        coll = {}
        coll["id"] = 0
        coll["idReader"] = "Server Exception"
        coll["idBook"] = str(170501)
        coll["bookName"] = str(e)
        coll["createTime"] = str(e)
        coll["operation"] = str(e)
        collections.append(coll)
        context['data'] = collections
        return JsonResponse(context)

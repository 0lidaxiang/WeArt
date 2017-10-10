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
        if not res:
            context['status'] = "fail"
            context['errorNumber'] = status
            context['message'] = "錯誤 : getMyCollection　寫入 collection 表錯誤。"
            return JsonResponse(context)

        context['status'] = "success"
        context['errorNumber'] = 170500
        collections = []
        for v in mes:
            coll = {}
            res,status,mes = book.getValue(v.idBook_id, "name")
            if res:
                coll["idColl"] = v.id
                coll["idReader"] = v.idReader_id
                coll["idBook"] = v.idBook_id
                coll["bookName"] = mes
                coll["createTime"] = v.createTime
            collections.append(coll)
        context['message'] = collections
        return JsonResponse(context)
    except Exception as e:
        context['status'] = "fail"
        context['errorNumber'] = 170501
        context['message'] = str(e)
        print str(e)
        return JsonResponse(context)

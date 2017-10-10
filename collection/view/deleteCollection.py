#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from collection.models import collection

def deleteObj(request):
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idCollectionArg = request.GET["idCollectionArg"]
    idReader = request.session["readerId"]
    context = {}
    try:
        res, status, mes = collection.deleteObj(idCollectionArg, idReader)
        if not res:
            context['status'] = "fail"
            context['errorNumber'] = status
            context['message'] = "錯誤 : delete　寫入 collection 表錯誤。"
            return context

        context['status'] = "success"
        context['errorNumber'] = 170600
        context['message'] = "添加成功．"
        return JsonResponse(context)
    except Exception as e:
        context['status'] = "fail"
        context['errorNumber'] = 170601
        context['message'] = str(e)
        print str(e)
        return JsonResponse(context)

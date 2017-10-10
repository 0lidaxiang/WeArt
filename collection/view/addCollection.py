#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from collection.models import collection

def goToAddCollection(request):
    context = {}
    idBook = request.GET["idBook"]

    if "readerId" not in request.session:
        lastUrl = request.GET["lastUrl"]

        context['status'] = "success1"
        context['message'] = "/reader/login/?lastUrl=" + "/collection/addCollectionInter/?idBook=" + idBook
        return JsonResponse(context)
    else:
        readerId = request.session["readerId"]

        context['status'] = "success2"
        context['message'] = idBook
        # context['message'] = "/collection/add/?idBook=" + idBook
        return JsonResponse(context)

def add(request):
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idBook = request.GET["idBook"]
    idReader = request.session["readerId"]
    context = {}
    try:
        res, status, mes = collection.add(idReader, idBook)
        # res, status, mes = collection.add(idBook, idReader)

        if not res:
            context['status'] = "fail"
            context['errorNumber'] = status
            context['message'] = "錯誤 : add　寫入 collection 表錯誤。"
            return JsonResponse(context)

        context['status'] = "success"
        context['errorNumber'] = 170400
        context['message'] = "添加成功．"
        return JsonResponse(context)
    except Exception as e:
        context['status'] = "fail"
        context['errorNumber'] = 170401
        context['message'] = str(e)
        print str(e)
        return JsonResponse(context)

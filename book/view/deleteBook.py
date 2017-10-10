#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from book.models import book

def deleteObj(request):
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idBook = request.GET["idBook"]
    idReader = request.session["readerId"]
    context = {}
    try:
        res, status, mes = book.deleteObj(idBook, idReader)
        if not res:
            context['status'] = "fail"
            context['statusNumber'] = status
            context['message'] = mes
            return JsonResponse(context)

        context['status'] = "success"
        context['statusNumber'] = 130600
        context['message'] = ""
        return JsonResponse(context)
    except Exception as e:
        context['status'] = "fail"
        context['statusNumber'] = 130601
        context['message'] = str(e)
        print str(e)
        return JsonResponse(context)

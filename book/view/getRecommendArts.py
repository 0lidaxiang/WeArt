#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import json
from django.http import JsonResponse

from django.shortcuts import render
from book.models import book

def getRecommendArts(request):
    context = {}
    reload(sys)
    sys.setdefaultencoding('utf8')

    # get the new book name of user input if it is not null
    if 'amount' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The amount variable is not in request.GET."
        return JsonResponse(context)
    inputAmount = request.GET['amount']

    res, statusNumber, mes = book.getAll(inputAmount)

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
        response_record['chapterCount'] = m.chapterCount
        response_record['idAuthor_id'] = m.idAuthor_id
        response_data.append(response_record)

    context["message"] = response_data

    return JsonResponse(context)

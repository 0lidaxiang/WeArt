#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import json
from django.http import JsonResponse

from django.shortcuts import render
from book.models import book
from recommend.models import recommend
from reader.models import reader

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

    # res, statusNumber, mes = book.getAll(inputAmount)
    res, statusNumber, mes = recommend.getAll(0)

    if not res:
        context['status'] = "fail"
        context['message'] = "錯誤： " + mes
        return JsonResponse(context)

    context['status'] = "success"

    response_data = []
    for rec in mes:
        obj = book.getValue(rec.idBook_id, "all")[2]
        response_record = {}
        response_record['id'] = obj.id
        response_record['name'] = obj.name
        response_record['chapterCount'] = obj.chapterCount
        response_record['author_name'] =  reader.getValueById(obj.idReader_id, "name")[2]
        response_data.append(response_record)

    context["message"] = response_data

    return JsonResponse(context)

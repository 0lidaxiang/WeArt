#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from django.shortcuts import render
from django.http import JsonResponse
from reader.models import reader
from reader.view.loginView import logout
from tool.tools import createId

def modifyReader(request):
    # dealing with Chinese questions
    reload(sys)
    sys.setdefaultencoding('utf8')

    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idReader = request.session["readerId"]
    argName = request.POST["argName"]
    value = request.POST["value"]
    context = {}
    try:
        if argName == "name":
            res, status, mes = reader.modifyObj(idReader, argName, value)
            if not res:
                context['res'] = "fail"
                context['statusNumber'] = str(status)
                context['message'] = "錯誤 : modifyReader　寫入 reader 表錯誤。"
                return JsonResponse(context)
            request.session["userName"] = value

        if argName == "passwd":
            res, status, mes = reader.modifyObj(idReader, argName, createId(96, value))
            if not res:
                context['res'] = "fail"
                context['statusNumber'] = str(status)
                context['message'] = "錯誤 : modifyReader　寫入 reader 表錯誤。"
                return JsonResponse(context)

            logout(request)
        context['res'] = "success"
        context['statusNumber'] = 110500
        context['message'] = ""
        return JsonResponse(context)
    except Exception as e:
        context['res'] = "fail"
        context['statusNumber'] = 110501
        context['message'] = str(e)
        print str(e)
        return JsonResponse(context)

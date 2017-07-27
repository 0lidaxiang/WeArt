#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from tool.tools import createId
from reader.models import reader
from django.views.decorators import csrf
from django.http import HttpResponse

# Create your views here.
def loginReader(request):
    passwd = createId(96,request.POST['password'])
    email = unicode(request.POST['email'])

    try:
        readerObj = reader.objects.get(email=email)
        if readerObj.status == "allowed":
            if passwd == readerObj.passwd:
                return render(request, 'reader/readerIndex.html')
            else:
                return render(request, 'reader/loginFail.html', {'message': u'密碼錯誤！請重新登錄！'})
        elif readerObj.status == "abuse":
            return render(request, 'reader/loginFail.html', {'message': u'您尚未驗證郵箱！請前往注冊郵箱驗證身份！'})
    except reader.DoesNotExist:
        return render(request, 'reader/loginFail.html', {'message': u'用戶不存在！請重新登錄！'})

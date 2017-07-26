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
                return render(request, 'reader/readerManage.html')
            else:
                return render(request, 'reader/loginFail.html', {'message': u'密码错误！请重新登录！'})
        elif readerObj.status == "abuse":
            return render(request, 'reader/loginFail.html', {'message': u'您尚未验证邮箱！请前往注册邮箱验证身份！'})
    except reader.DoesNotExist:
        return render(request, 'reader/loginFail.html', {'message': u'用户不存在！请重新登录！'})

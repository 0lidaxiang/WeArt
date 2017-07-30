#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
# from django.contrib.auth.decorators import login_required

from tool.tools import createId
from reader.models import reader
from author.models import author


# connect to mysql and check
def loginReader(request):
    if "readerId" in request.session:
        return render(request, 'reader/readerIndex.html')
    else:
        if 'email' in request.POST and  'password' in request.POST :
            email = unicode(request.POST['email'])
            passwd = createId(96,request.POST['password'])
            try:
                readerObj = reader.objects.get(email=email)
                if readerObj.status == "allowed":
                    if passwd == readerObj.passwd:
                        request.session["readerId"] = readerObj.id

                        # check user is or not author and author's status
                        isAuthor = author.isExistIdReader(readerObj.id)
                        request.session["isAuthor"] = isAuthor
                        authorStatus = author.getStatus(readerObj.id)
                        if isAuthor:
                            if authorStatus == "active":
                                request.session["authorStatus"] = "active"
                            else:
                                request.session["authorStatus"] = authorStatus
                        else:
                            request.session["authorStatus"] = ""
                        return render(request, 'reader/readerIndex.html')
                    else:
                        return render(request, 'reader/loginFail.html', {'message': u'密碼錯誤！請重新登錄！'})
                elif readerObj.status == "abuse":
                    return render(request, 'reader/loginFail.html', {'message': u'您尚未驗證郵箱！請前往注冊郵箱驗證身份！'})
            except reader.DoesNotExist:
                return render(request, 'reader/loginFail.html', {'message': u'用戶不存在！請重新登錄！'})
        else:
            return render(request, 'reader/login.html')


def logout(request):
    if "readerId" in request.session:
        # delete session
        del request.session["readerId"] # if not exists, report error
        del request.session["isAuthor"] # if not exists, report error
        request.session.flush()
        return render(request, 'reader/login.html')
    else:
        return render(request, 'reader/login.html')
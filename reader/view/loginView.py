#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
# from django.contrib.auth.decorators import login_required

from tool.tools import createId
from reader.models import reader
from author.models import author


# connect to mysql and check
def loginReader(request):
    lastUrl = ""
    if "lastUrl" in request.POST:
        lastUrl = request.POST['lastUrl']

    context = {}
    if "readerId" in request.session:
        context['status'] = "success"
        if lastUrl == "null":
            # context['message'] = "/reader/readerIndex/"
            return HttpResponseRedirect("/reader/index/")
        elif lastUrl == "" or lastUrl is None:
            context['status'] = "fail"
            context['message'] = "錯誤的訪問"
            return JsonResponse(context)
        else:
            # context['message'] = lastUrl
            return HttpResponseRedirect(lastUrl)
        # return JsonResponse(context)

    if 'userName' not in request.POST and  'passwd' not in request.POST :
        context['status'] = "fail"
        context['message'] = "請重載後輸入 Email 和密碼"
        return JsonResponse(context)
        # return render(request, 'reader/login.html')

    userName = unicode(request.POST['userName'])
    passwd = createId(96,request.POST['passwd'])

    try:
        readerObj = reader.objects.get(email=userName)
        if readerObj.status == "allowed":
            if passwd != readerObj.passwd:
                context['status'] = "fail"
                context['message'] = "密碼錯誤！請重新登錄！"
                return JsonResponse(context)
                # return render(request, 'reader/loginFail.html', {'message': u'密碼錯誤！請重新登錄！'})

            request.session["readerId"] = readerObj.id
            request.session["userName"] = readerObj.name

            # check user is or not author and author's status
            isAuthor = author.isExist(readerObj.id)
            request.session["isAuthor"] = isAuthor
            authorStatus = author.getStatus(readerObj.id)
            if not isAuthor:
                request.session["authorStatus"] = ""
                context['status'] = "success"
                if lastUrl == "null":
                    context['message'] = "/reader/index/"
                else:
                    context['message'] = lastUrl
                return JsonResponse(context)


            authorId = author.getId(readerObj.id)
            if authorId != "":
                request.session["authorId"] = authorId
            if authorStatus == "active":
                request.session["authorStatus"] = "active"
            else:
                request.session["authorStatus"] = authorStatus

            context['status'] = "success"

            if lastUrl == "null":
                context['message'] = "/reader/index/"
            else:
                context['message'] = lastUrl
            return JsonResponse(context)

        elif readerObj.status == "abuse":
            context['status'] = "fail"
            context['message'] = "您尚未驗證郵箱！請前往注冊郵箱驗證身份！"
            return JsonResponse(context)
        else :
            context['status'] = "fail"
            context['message'] = '您的帳號狀態異常，無法登錄，目前狀態爲：' + str(readerObj.status) + '請聯繫管理員或重新註冊。'
            return JsonResponse(context)
    except reader.DoesNotExist:
        context['status'] = "fail"
        context['message'] = '用戶不存在！請重新登錄！'
        return JsonResponse(context)

def logout(request):
    # delete session
    if "readerId" in request.session:
        del request.session["readerId"] # if not exists, report error
        del request.session["userName"] # if not exists, report error
        del request.session["isAuthor"] # if not exists, report error

        if 'authorId' in request.session:
            del request.session["authorId"] # if not exists, report error

        del request.session["authorStatus"] # if not exists, report error

        request.session.flush()

        return HttpResponseRedirect('/reader/login/')
    else:
        return HttpResponseRedirect('/reader/login/')

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
from time import localtime, strftime

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.views.decorators import csrf
from time import localtime,strftime
# from django.conf import settings

from tool.Token import *
from tool.tools import *
from reader.models import reader

#this need catch the id
#catch the "name"
def registerReader(request):
    if "userName" not in request.POST:
        return render(request, 'reader/register.html')
    if "password" not in request.POST:
        return render(request, 'reader/register.html')
    if "email" not in request.POST:
        return render(request, 'reader/register.html')

    userName =  unicode(request.POST['userName'])
    password = request.POST['password']
    email = unicode(request.POST['email'])
    nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(userName,password,email)
    userName = userName.encode('utf8')
    try:
        res, statusNumber, message = reader.getValueByEmail(email, "status")
        if not res:
            idVal = createId(20, userName + email)
            passwordEncrypted = createId(96,password)
            res, statusNumber, message = reader.add(idVal, userName, passwordEncrypted, email, "abuse", nowTime)

            if not res:
                return render(request, 'reader/registerFail.html', {'message': u"註冊失敗！請重新嘗試或聯絡管理員" + str(statusNumber) + " : " + message})

            if sendVerifyEmail(userName, email):
                return render(request, 'reader/registerVerificating.html')
            else:
                return render(request, 'reader/registerFail.html', {'message': u"發送郵件失敗！請更換郵箱地址重新注冊或聯繫管理員！"})

        if message == "abuse":
            if sendVerifyEmail(userName, email):
                return render(request, 'reader/registerVerificating.html')
            else:
                return render(request, 'reader/registerFail.html', {'message': u"發送郵件失敗！請更換郵箱地址重新注冊或聯繫管理員！"})
        else:
            return render(request, 'reader/registerFail.html', {'message': u"您填寫的郵箱已經被注冊！請更換郵箱地址重新注冊！"})
    except Exception as e:
        print e
        return render(request, 'reader/registerFail.html', {'message': u"註冊失敗！請重新嘗試或聯絡管理員" + str(e)})

def sendVerifyEmail(userName, email):
    try:
        token_confirm = Token(django_settings.SECRET_KEY)
        token = token_confirm.generate_validate_token(email)

        # port 80
        ipAddress = django_settings.REGISTER_SERVER_DOMAIN
        message = "\n".join([u'{0} , 歡迎加入 WeArt !'.format(userName), u'\n\n請訪問以下鏈接，完成用戶驗證:', '/'.join([ipAddress,'reader/activate',token]), u'\n\n如果您沒有注冊 WeArt，請忽略該郵件！',])

        send_mail(
            'WeArt注冊身份驗證',
            message,
            'weartregister@gmail.com',
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print e
        return False

def activeReader(request, token):
    token_confirm = Token(django_settings.SECRET_KEY)
    try:
        emailSignature = token_confirm.confirm_validate_token(token)
    except:
        #delete this user's Token
        emailSignature = token_confirm.remove_validate_token(token)

        # users = reader.objects.filter(email=emailSignature)
        res, statusNumber, message = reader.deleteObj("email", emailSignature)
        if not res:
            return render(request, 'reader/registerFail.html', {'message': u"驗證中獲取 reader info 失敗！請重新嘗試或聯絡管理員" + str(statusNumber) + " : " + message})
        return render(request, 'reader/registerFail.html', {'message': u'對不起，驗證鏈接已經過期！請重新注冊！'})

    try:
        readerObj = reader.objects.get(email=emailSignature)
    except reader.DoesNotExist:
        return render(request, 'reader/registerFail.html', {'message': u"對不起，您所驗證的用戶不存在！請重新注冊！"})
    readerObj.status = "allowed"
    readerObj.save()
    return render(request, 'reader/registerSuccess.html')

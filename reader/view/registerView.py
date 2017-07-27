#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from time import gmtime, strftime
from django.conf import settings as django_settings
from django.core.mail import send_mail
from tool.Token import *
from tool.tools import *
from django.views.decorators import csrf
from reader.models import reader

def registerReader(request):
    userName =  unicode(request.POST['userName'])
    password = request.POST['password']
    email = unicode(request.POST['email'])
    nowTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    try:
        readerObj = reader.objects.get(email=email)
        return render(request, 'reader/registerFail.html', {'message': u"您填寫的郵箱已經被注冊！請更換郵箱地址重新注冊！"})
    except reader.DoesNotExist:
        test1 = reader(id = createId(20, userName),name = userName,passwd = createId(96,password),email = email,status = "abuse",createTime = nowTime)
        test1.save()

        username = userName.encode('utf8')
        token_confirm = Token(django_settings.SECRET_KEY)
        token = token_confirm.generate_validate_token(email)
        message = "\n".join([u'{0} , 歡迎加入 WeArt !'.format(username), u'\n\n請訪問以下鏈接，完成用戶驗證:', '/'.join([django_settings.DOMAIN,'reader/activate',token]), u'\n\n如果您沒有注冊 WeArt，請忽略該郵件！',])

        send_mail(
            'WeArt注冊身份驗證',
            message,
            'weartregister@gmail.com',
            [email],
            fail_silently=False,
        )

        return render(request, 'reader/registerVerificating.html')

def activeReader(request, token):
    token_confirm = Token(django_settings.SECRET_KEY)
    try:
        emailSignature = token_confirm.confirm_validate_token(token)
    except:
        emailSignature = token_confirm.remove_validate_token(token)
        users = reader.objects.filter(email=emailSignature)
        for user in users:
	           user.delete()
        return render(request, 'reader/registerFail.html', {'message': u'對不起，驗證鏈接已經過期！請重新注冊！'})
    try:
        readerObj = reader.objects.get(email=emailSignature)
    except reader.DoesNotExist:
        return render(request, 'reader/registerFail.html', {'message': u"對不起，您所驗證的用戶不存在！請重新注冊！"})
    readerObj.status = "allowed"
    readerObj.save()
    return render(request, 'reader/registerSuccess.html')

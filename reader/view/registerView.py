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
        return render(request, 'reader/registerFail.html', {'message': u"您填写的邮箱已经被注册！请更换邮箱地址重新注册！"})
    except reader.DoesNotExist:
        test1 = reader(id = createId(20, userName),name = userName,passwd = createId(96,password),email = email,status = "abuse",createTime = nowTime)
        test1.save()

        username = userName.encode('utf8')
        token_confirm = Token(django_settings.SECRET_KEY)
        token = token_confirm.generate_validate_token(email)
        message = "\n".join([u'{0} , 欢迎加入 WeArt !'.format(username), u'\n\n请访问以下链接，完成用户验证:', '/'.join([django_settings.DOMAIN,'reader/activate',token]), u'\n\n如果您没有注册 WeArt，请忽略该邮件！',])

        send_mail(
            'WeArt注册身份验证',
            message,
            'weartregister@gmail.com',
            ['0lidaxiang@gmail.com'],
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
        return render(request, 'reader/registerFail.html', {'message': u'对不起，验证链接已经过期！请重新注册！'})
    try:
        readerObj = reader.objects.get(email=emailSignature)
    except reader.DoesNotExist:
        return render(request, 'reader/registerFail.html', {'message': u"对不起，您所验证的用户不存在！请重新注册！"})
    readerObj.status = "allowed"
    readerObj.save()
    return render(request, 'reader/registerSuccess.html')

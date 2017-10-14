#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import subprocess
import paramiko

from django.shortcuts import render
from django.http import JsonResponse

from book.models import book
from django.conf import settings

def deleteObj(request):
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    idBook = request.GET["idBook"]
    idReader = request.session["readerId"]
    context = {}
    try:
        # delete book's data in database and get its directory location
        res, statusNumber, mes = book.deleteObj(idBook)
        if not res:
            context['res'] = "fail"
            context['statusNumber'] = statusNumber
            context['message'] = mes
            return JsonResponse(context)
        path = mes + "/"
        operateDirName = idBook

        # rm the repo directory in webServer
        res, statusNumber, mes = rmDirOfWebServer(path, operateDirName)
        if not res:
            context['res'] = "fail"
            context['statusNumber'] = statusNumber
            context['message'] = mes
            return JsonResponse(context)

        # rm the repo directory in gitServer
        gitserver_ip = settings.GIT_SERVER_IP
        gitserver_user = settings.GIT_SERVER_USER
        gitserver_userPasswd = settings.GIT_SERVER_USERPASSWD
        res, statusNumber, mes = rmDirOfGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd, path, operateDirName)
        if not res:
            context['res'] = "fail"
            context['statusNumber'] = statusNumber
            context['message'] = mes
            return JsonResponse(context)

        context['res'] = "success"
        context['statusNumber'] = 130600
        context['message'] = ""
    except Exception as e:
        context['res'] = "fail"
        context['statusNumber'] = 130601
        context['message'] = str(e)
        print str(e)
    return JsonResponse(context)

def rmDirOfWebServer(path, operateDir):
    try:
        cmd = "rm -rf " + path + operateDir
        p = subprocess.Popen(cmd, shell=True)
        (stdoutput,erroutput) = p.communicate()
        return True, 130700, ""
    except Exception as e:
        print str(e)
        return False, 130701, str(e)

def rmDirOfGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd, path, operateDir):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(gitserver_ip,22,gitserver_user, gitserver_userPasswd,timeout=5)

        cmd = "rm -rf " + path + operateDir + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()
        return True, 130800, ""
    except Exception as e:
        print str(e)
        return False, 130801, str(e)

#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from author.models import author
from subprocess import Popen, PIPE, check_call
from django.conf import settings
import paramiko
import datetime
import os

def gotoReaderPages(request, pageName):
    # when login, it will check reader's status after readerId
    if "readerId" in request.session:
        return 'reader/' + pageName + '.html'
    else:
        return 'reader/login.html'

def readerIndex(request):
    return render(request,  gotoReaderPages(request, "readerIndex"))

def booksRecorded(request):
    return render(request,  gotoReaderPages(request, "booksRecorded"))

def readingHistory(request):
    return render(request,  gotoReaderPages(request, "readingHistory"))

def readerSetting(request):
    return render(request,  gotoReaderPages(request, "readerSetting"))

def getEnableAuthorStatus(request):
    try:
        if "readerId" in request.session:
            readerId = request.session["readerId"]

            data = {}
            data['status'] = 'success'
            isAuthor = False
            authorStatus = ""
            if author.isExistIdReader(readerId):
                isAuthor = True
                request.session["isAuthor"] = True

                # authorStatus maybe active or inactive or banned
                authorStatus = author.getStatus(readerId)
                if authorStatus:
                    request.session["authorStatus"] = authorStatus
                else:
                    request.session["authorStatus"] = ""
            data["isAuthor"] = isAuthor
            data["authorStatus"] = authorStatus

            return JsonResponse(data)
        else:
            data['status'] = 'fail'
            return render(request, 'reader/login.html')
    except Exception as e:
        data['status'] = 'fail'
        return JsonResponse(data)

def modifyAuthorStatus(request):
    status = ""
    if request.POST:
        status = request.POST['status']

    if "readerId" in request.session:
        data = {}

        try:
            readerId = request.session["readerId"]
            data['status'] = 'success'
            # check thatreader is or is not a author
            if author.isExistIdReader(readerId):
                # when reader is a author
                request.session["isAuthor"] = True
                data['isAuthor'] = True

                authorStatus = author.getStatus(readerId)
                # check author status
                if authorStatus == "active":
                    # disable author function when reader is registed and status is "active"
                    # step: modify the value of author's status in database
                    result = author.modifyStatus(readerId, status)
                    if result:
                        request.session["authorStatus"] = status
                        data['authorStatus'] = status #"inactive"
                    else:
                        data['authorStatus'] = request.session["authorStatus"]
                elif authorStatus == "inactive":
                    # files operating result
                    statusTemp,authorStatusTemp,messageTemp = activeAuthorFunction(request,readerId)
                    data['status'] = statusTemp
                    data['authorStatus'] = authorStatusTemp
                    data['message'] = messageTemp
                    request.session["authorStatus"] = authorStatusTemp
                else:
                    # request.session["authorStatus"] = authorStatus
                    # data['authorStatus'] = authorStatus
                    data['status'] = "fail"
                    data['authorStatus'] = authorStatus
                    data['message'] = "讀取作者狀態異常!"
                    request.session["authorStatus"] = authorStatus
            else:
                # when reader is not a author
                # step1: add data to table "author"
                # step2: active author (mkdir in git server)
                if  author.addAuthor(readerId):
                    # database operating result
                    data['isAuthor'] = True
                    request.session["isAuthor"] = True

                    # files operating result
                    statusTemp,authorStatusTemp,messageTemp = activeAuthorFunction(request,readerId)
                    data['status'] = statusTemp
                    data['authorStatus'] = authorStatusTemp
                    data['message'] = messageTemp
                    request.session["authorStatus"] = authorStatusTemp
                else:
                    request.session["isAuthor"] = False
        except Exception as e:
            data['status'] = 'fail'
            data['message'] = str(e)
        return JsonResponse(data)
    else:
        return render(request, 'reader/login.html')

def activeAuthorFunction(request,readerId):
    # enable author function when reader is registed and status is "inactive"
    # step1: mkdir in git server
    res,mes = mkClassedDirInGitServer()
    if res:
        # statp2: modify the value of author's status in database
        result = author.modifyStatus(readerId, "active")
        if result:
            # return status,authorStatus,message
            return "success","active",mes
        else:
            # return status,authorStatus,message
            return "success","active",mes
    else:
        # return status,authorStatus,message
        return "fail","inactive",mes

def mkClassedDirInGitServer():
    gitserver_ip = settings.GIT_SERVER_IP
    gitserver_user = settings.GIT_SERVER_USER
    gitserver_userPasswd = settings.GIT_SERVER_USERPASSWD
    script_mkdir = settings.SCRIPT_MKDIR
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # conncet to server
        ssh.connect(gitserver_ip,22,gitserver_user, gitserver_userPasswd,timeout=5)
        cmd = "cd ~;python " + script_mkdir
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        ssh.close()
        return True,""
    except Exception as e:
        return False,str(e)

# def addUserInWebAndGitServer(authorId, passwd):
#     gitserver_ip = settings.GIT_SERVER_IP
#     loginUserName = "root"
#     loginPasswd = "lidaxiang"
#
#     groupName = "author"
#     userName = authorId
#     passwd = passwd
#     print userName
#     print passwd
#
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#         # git init to create remote repo in gitServer
#         ssh.connect(gitserver_ip,22,loginUserName, loginPasswd,timeout=5)
#         cmd = "useradd -m -g " + groupName + " " + userName
#         ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
#         cmd = "passwd"
#         ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
#         ssh_stdin.write(passwd)
#         ssh_stdin.write(passwd)
#         ssh.close()
#         return True
#     except Exception as e:
#         return False

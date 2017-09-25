#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from book.models import book

import paramiko
import sys
import json
import os
import datetime
import subprocess

def createABook(request):
    context = {}
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    if request.session["authorStatus"] != "active":
        return render(request, 'author/authorStatus/')

    reload(sys)
    sys.setdefaultencoding('utf8')

    readerId = request.session["readerId"]

    serverHomeDir = "/home/lidaxiang"

    # get the new book name of user input if it is not null
    if 'newBookName' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The newBookName variable is not in request.GET."
        return JsonResponse(context)
    userInputBookName = request.GET['newBookName']

    if userInputBookName == "":
        context['status'] = "fail"
        context['message'] = "您還沒有填寫新書名稱。請重載後重新嘗試。"
        return JsonResponse(context)

    try:
        # check whether a book is exist by bookname and idReader_id  before writing data into database
        # readerId = request.session['readerId']
        res, statusNumber, mes = book.getIdByNameAndAuthor(userInputBookName, readerId)
        if res:
            context['status'] = "fail"
            context['message'] = "已經存在該本書！請重新輸入其它書名或登錄其它賬號"
            return JsonResponse(context)

        # this author dont have this book
        if statusNumber == 130004:
            gitserver_ip = settings.GIT_SERVER_IP
            gitserver_user = settings.GIT_SERVER_USER
            gitserver_userPasswd = settings.GIT_SERVER_USERPASSWD

            # step1: struct the parent directory name
            now = datetime.datetime.now()
            monthClassedDirName = serverHomeDir + "/" + str(now.year) + "/" + str(now.month)

            # step2: write data into database
            res,mes = book.add(userInputBookName, gitserver_ip, monthClassedDirName, readerId)
            if not res:
                # This needs to delete the all folder
                # This needs to delete the data in database if exists.

                context['status'] = "fail"
                context['message'] = '創建 《' + userInputBookName + "》失敗，添加到 Database 中失敗。" + mes + "。請刷新後重試！"
                return JsonResponse(context)
            idBook = mes

            # step3: make directory in gitServer
            res,mes = mkClassedDirInGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd, serverHomeDir, idBook)
            if not res:
                context['status'] = "fail"
                context['message'] = "錯誤： " + mes
                return JsonResponse(context)

            # step3: git init this book's repo in gitServer
            res,mes = gitInitInGitServer(gitserver_ip,gitserver_user,gitserver_userPasswd,monthClassedDirName,idBook)
            if not res:
                # This needs to delete the all folder

                # return front-end
                context['status'] = "fail"
                context['message'] = "創建新書失敗！請刷新後重試！" + mes
                return JsonResponse(context)

            # step3: check and make the parent directory in webServer
            res,mes = mkClassedDirInWebServer(serverHomeDir)
            if not res:
                # This needs to delete the all folder

                # return front-end when making directory in Web Server  failed
                context['status'] = "fail"
                context['message'] = "Git Clone Failed！" + mes
                return JsonResponse(context)

            # step3: git clone from gitServer
            clone_path = gitserver_user + "@" + gitserver_ip + ":" + monthClassedDirName + "/" + idBook + ".git"
            clone_cmd = " git clone " + clone_path
            os.chdir(monthClassedDirName)
            os.system("sshpass -p " + gitserver_userPasswd + clone_cmd)

            context['status'] = "success"
            context['message'] = '您已經成功創建 《' + userInputBookName + "》。請點選左側菜單功能來創建您的章節。"

        elif statusNumber == 130005:
            context['status'] = "fail"
            context['message'] = "未知服務器錯誤：" + str(statusNumber) + mes
        else:
            context['status'] = "fail"
            context['message'] = "其它服務器錯誤：" + str(statusNumber) + mes

    except Exception as e:
        context['status'] = "fail"
        context['message'] = "異常錯誤: " + str(e)
    return JsonResponse(context)

def mkClassedDirInWebServer(operateDir):
    script_mkdir = settings.SCRIPT_MKDIR
    try:
        cmd = "cd " + operateDir + ";python " + script_mkdir
        p = subprocess.Popen(cmd, shell=True)
        (stdoutput,erroutput) = p.communicate()
        return True,""
    except Exception as e:
        return False,str(e)

def mkClassedDirInGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd, operateDir, idBook):
    script_mkdir = settings.SCRIPT_MKDIR

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # conncet to server
        ssh.connect(gitserver_ip,22,gitserver_user, gitserver_userPasswd,timeout=5)

        cmd = "cd " + operateDir + ";python " + script_mkdir
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()
        return True,""
    except Exception as e:
        return False,str(e)

def gitInitInGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd,monthClassedDirName,idBook):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # conncet to server
        ssh.connect(gitserver_ip,22,gitserver_user, gitserver_userPasswd,timeout=5)

        cmd = "cd " + monthClassedDirName + ";mkdir " + idBook + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        cmd = "git init --bare " + monthClassedDirName + "/" + idBook + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()
        return True,""
    except Exception as e:
        return False,str(e)

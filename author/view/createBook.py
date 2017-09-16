#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from author.models import author
from book.models import book

import paramiko
import sys
import json
import os
import datetime
import subprocess

def createABook(request):
    context = {}
    if "readerId" in request.session:
        if request.session["authorStatus"] == "active":
            reload(sys)
            sys.setdefaultencoding('utf8')

            readerId = request.session["readerId"]
            # get this user's account
            # authorStatus = author.getStatus(readerId)

            # loginId = "lidaxiang"
            # loginpasswd = "lidaxiang"

            # serverHomeDir = "/home/" + loginId
            serverHomeDir = "/home/lidaxiang"

            # get new book name and create respository in remote server
            request.encoding='utf-8'
            idBook = ""
            if 'newBookName' in request.GET:
                userInputBookName = request.GET['newBookName']

                try:
                    if userInputBookName == "":
                        context['status'] = "fail"
                        context['message'] = "The idBook is null."
                    else:
                        authorId = request.session['authorId']

                        # check whether a book is exist by bookname and idAuthor_id  before writing data into database
                        res, statusNumber, idBook = book.getIdByNameAndAuthor(userInputBookName, authorId)
                        if res:
                            context['status'] = "fail"
                            context['message'] = "已經存在該本書！請重新確定您輸入的書名和賬號"
                        else:
                            if statusNumber == 130004:
                                # this author dont have this book
                                # can create this book for this author

                                # gitserver_ip needs changes when changing git server
                                gitserver_ip = settings.GIT_SERVER_IP
                                gitserver_user = settings.GIT_SERVER_USER
                                gitserver_userPasswd = settings.GIT_SERVER_USERPASSWD

                                now = datetime.datetime.now()
                                monthClassedDirName = serverHomeDir + "/" + str(now.year) + "/" + str(now.month)
                                # localMonthClassedDir= serverHomeDir + "/" + str(now.year) + "/" + str(now.month)

                                # write data into database
                                res,mes = book.add(userInputBookName, gitserver_ip, monthClassedDirName, authorId)
                                if res:
                                    idBook = mes

                                    ssh = paramiko.SSHClient()
                                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                                    # make directory in gitServer
                                    res,mes = mkClassedDirInGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd, serverHomeDir, idBook)
                                    if res:
                                        # git init in gitServer
                                        res,mes = gitInitInGitServer(gitserver_ip,gitserver_user,gitserver_userPasswd,monthClassedDirName,idBook)
                                        if res:
                                            # make directory webServer
                                            res,mes = mkClassedDirInWebServer(serverHomeDir)
                                            if res:
                                                # git clone from gitServer
                                                clone_path = gitserver_user + "@" + gitserver_ip + ":" + monthClassedDirName + "/" + idBook + ".git"
                                                clone_cmd = " git clone " + clone_path
                                                os.chdir(monthClassedDirName)
                                                os.system("sshpass -p " + gitserver_userPasswd + clone_cmd)

                                                context['status'] = "success"
                                                context['message'] = '您已經成功創建 《' + userInputBookName + "》。請點選左側菜單功能來創建您的章節。"
                                            else:
                                                # This needs to delete the all folder

                                                # return front-end when making directory in Web Server  failed
                                                context['status'] = "fail"
                                                context['message'] = "Git Clone Failed！" + mes
                                        else:
                                            # This needs to delete the all folder

                                            # return front-end
                                            context['status'] = "fail"
                                            context['message'] = "創建新書失敗！請刷新後重試！" + mes
                                    else:
                                        context['status'] = "fail"
                                        context['message'] = mes
                                else:
                                    # This needs to delete the all folder
                                    # This needs to delete the data in database if exists.

                                    context['status'] = "fail"
                                    context['message'] = '創建 《' + userInputBookName + "》失敗。" + mes + "。請刷新後重試！"
                            elif statusNumber == 130005:
                                context['status'] = "fail"
                                context['message'] = "未知服務器錯誤：" + statusNumber + mes
                            else:
                                context['status'] = "fail"
                                context['message'] = "其它服務器錯誤：" + statusNumber + mes
                except Exception as e:
                    context['status'] = "fail"
                    context['message'] = str(e)
            else:
                context['status'] = "fail"
                context['message'] = "您還沒有填寫新書名稱。請重載後重新嘗試。"
            return JsonResponse(context)
        else:
            return render(request, 'author/authorStatus/')

    else:
        return render(request, 'reader/login.html')

def mkClassedDirInWebServer(operateDir):
    script_mkdir = settings.SCRIPT_MKDIR
    try:
        # cmd = "git config --global user.email user1@gmail.com; git config --global user.name user1"
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

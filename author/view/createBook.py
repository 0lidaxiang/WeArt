# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from git import Repo
from author.models import author

# import time
# import subprocess
import paramiko
import sys
import json
import os
import shutil
import datetime

def createABook(request):
    context = {}
    if "readerId" in request.session:
        if request.session["authorStatus"] == "active":
            reload(sys)
            sys.setdefaultencoding('utf8')

            readerId = request.session["readerId"]
            # get this user's account
            # authorStatus = author.getStatus(readerId)
            loginId = "lidaxiang"
            loginpasswd = "lidaxiang"

            # get new book name and create respository in remote server
            request.encoding='utf-8'
            bookName = ""
            if 'newBookName' in request.GET:
                bookName = request.GET['newBookName']
                try:
                    if bookName == "":
                        context['status'] = "fail"
                        context['message'] = "The bookName is null."
                    else:
                        # gitserver_ip needs changes when changing git server
                        gitserver_ip = settings.GIT_SERVER_IP_1
                        gitserver_user = settings.GIT_SERVER_USER
                        gitserver_userPasswd = settings.GIT_SERVER_USERPASSWD

                        print gitserver_user
                        print gitserver_userPasswd

                        now = datetime.datetime.now()
                        monthClassedDirName = "/home/" + gitserver_user + "/" + str(now.year) + "/" + str(now.month)

                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                        # git init to create remote repo in gitServer
                        res,mes = mkClassedDirInGitServer(gitserver_ip,gitserver_user,gitserver_userPasswd,monthClassedDirName,bookName)
                        if res:
                            # git clone in webServer
                            myhome_path = "/home/" + loginId
                            clone_path = gitserver_user + "@" + gitserver_ip + ":" + monthClassedDirName + "/" + bookName + ".git"
                            clone_cmd = " git clone " + clone_path
                            os.chdir(myhome_path)
                            os.system("sshpass -p " + gitserver_userPasswd + clone_cmd)

                            context['status'] = "success"
                            context['message'] = '您已經成功創建 《' + bookName + "》。請點選左側菜單功能來創建您的章節。"
                        else:
                            context['status'] = "fail"
                            context['message'] = mes
                        return JsonResponse(context)

                except Exception as e:
                    context['status'] = "fail"
                    context['message'] = str(e)
                    return JsonResponse(context)
            else:
                context['status'] = "fail"
                context['message'] = "您還沒有填寫新書名稱。請重載後重新嘗試。"
                return JsonResponse(context)
        else:
            return render(request, 'author/authorStatus/')

    else:
        return render(request, 'reader/login.html')

def mkClassedDirInGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd,monthClassedDirName,bookName):
    # loginName = "lidaxiang"
    script_mkdir = settings.SCRIPT_MKDIR

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # conncet to server
        ssh.connect(gitserver_ip,22,gitserver_user, gitserver_userPasswd,timeout=5)
        cmd = "cd ~;python " + script_mkdir
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        cmd = "cd " + monthClassedDirName + ";mkdir " + bookName + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        cmd = "git init --bare " + monthClassedDirName + "/" + bookName + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()
        return True,""
    except Exception as e:
        return False,str(e)

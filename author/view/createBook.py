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
            loginId = "lidaxiang"
            loginpasswd = "lidaxiang"

            # get new book name and create respository in remote server
            request.encoding='utf-8'
            bookName = ""
            if 'newBookName' in request.GET:
                userInputBookName = request.GET['newBookName']
                bookName = request.session['authorId'] + "_" + userInputBookName

                try:
                    if bookName == "":
                        context['status'] = "fail"
                        context['message'] = "The bookName is null."
                    else:
                        # gitserver_ip needs changes when changing git server
                        gitserver_ip = settings.GIT_SERVER_IP_1
                        gitserver_user = settings.GIT_SERVER_USER
                        gitserver_userPasswd = settings.GIT_SERVER_USERPASSWD

                        now = datetime.datetime.now()
                        monthClassedDirName = "/home/" + gitserver_user + "/" + str(now.year) + "/" + str(now.month)
                        localMonthClassedDir= "/home/" + "lidaxiang" + "/" + str(now.year) + "/" + str(now.month)

                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                        # make directory in gitServer
                        res,mes = mkClassedDirInGitServer(gitserver_ip,gitserver_user,gitserver_userPasswd,monthClassedDirName,bookName)
                        if res:
                            # git init in gitServer
                            res,mes = gitInitInGitServer(gitserver_ip,gitserver_user,gitserver_userPasswd,monthClassedDirName,bookName)
                            if res:
                                # make directory webServer
                                res,mes = mkClassedDirInWebServer()
                                if res:
                                    # git clone from gitServer
                                    clone_path = gitserver_user + "@" + gitserver_ip + ":" + monthClassedDirName + "/" + bookName + ".git"
                                    clone_cmd = " git clone " + clone_path
                                    os.chdir(localMonthClassedDir)
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

def mkClassedDirInWebServer():
    # loginName = "lidaxiang"
    script_mkdir = settings.SCRIPT_MKDIR
    loginId = "lidaxiang"

    try:
        # cmd = "git config --global user.email user1@gmail.com; git config --global user.name user1"
        cmd = "cd /home/" + loginId + ";python " + script_mkdir
        p = subprocess.Popen(cmd, shell=True)
        (stdoutput,erroutput) = p.communicate()
        return True,""
    except Exception as e:
        return False,str(e)

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

        cmd = "git init --bare " + monthClassedDirName + "/" + bookName + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()
        return True,""
    except Exception as e:
        return False,str(e)

def gitInitInGitServer(gitserver_ip, gitserver_user, gitserver_userPasswd,monthClassedDirName,bookName):
    # loginName = "lidaxiang"
    script_mkdir = settings.SCRIPT_MKDIR
    print monthClassedDirName

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # conncet to server
        ssh.connect(gitserver_ip,22,gitserver_user, gitserver_userPasswd,timeout=5)

        cmd = "cd " + monthClassedDirName + ";mkdir " + bookName + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        cmd = "git init --bare " + monthClassedDirName + "/" + bookName + ".git"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()
        return True,""
    except Exception as e:
        return False,str(e)

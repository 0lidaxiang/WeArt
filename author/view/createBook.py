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
                        gitserver_ip = settings.GIT_SERVER_IP
                        authorId = author.getId(readerId)
                        authorPasswd = author.getPasswd(authorId)
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                        # git init to create remote repo in gitServer
                        ssh.connect(gitserver_ip,22,authorId, authorPasswd,timeout=5)
                        cmd = "cd ~;mkdir " + bookName + ".git"
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                        cmd = "git init --bare /home/" + authorId + "/" + bookName + ".git"
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                        ssh.close()

                        # git clone in webServer
                        myhome_path = "/home/" + loginId
                        clone_path = authorId + "@" + gitserver_ip + ":/home/" + authorId + "/" + bookName + ".git"
                        clone_cmd = " git clone " + clone_path
                        os.chdir(myhome_path)
                        os.system("sshpass -p " + authorPasswd + clone_cmd)

                        context['status'] = "success"
                        context['message'] = '您已經成功創建 《' + bookName + "》。請點選左側菜單功能來創建您的章節。"
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

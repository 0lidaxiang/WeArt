# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
import subprocess
import paramiko
import sys
from git import Repo
import json

def createABook(request):
    if "readerId" in request.session:
        reload(sys)
        sys.setdefaultencoding('utf8')
        context = {}

        # get this user's account
        loginId = "lidaxiang"
        loginpasswd = "lidaxiang"

        # get new book name and create respository in remote server
        request.encoding='utf-8'
        bookname = ""
        if 'newbookname' in request.GET:
            bookname = request.GET['newbookname']
        else:
            bookname = ""

        gitserver_ip = "192.168.122.149"
        username = "git"
        git_server_passwd = "git"
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(gitserver_ip,22,username, git_server_passwd,timeout=5)
            if bookname == "":
                context['mes_success'] = 'failed'
                return render(request, 'result.html', context)
            else:
                cmd = "cd ~;mkdir " + bookname + ".git"
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

                cmd = "cd ~" + "/" + bookname + ".git;""git init --bare "
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                ssh.close()

                # user the loginId got above to clone the remove new book respository
                p=subprocess.Popen("su "+loginId, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdoutput,erroutput) = p.communicate(input=loginpasswd)

                if erroutput.find("does not exist") > -1:
                    context['mes_success'] = 'does not exist user named ' + loginId + "."
                    return render(request, 'result.html', context)
                else:
                    context['mes_success'] = 'Your new book 《' + bookname + "》 is created success." + " " + stdoutput
                    myhome_path = "/home/" + loginId
                    p_cd_myhome = subprocess.Popen("cd " + myhome_path, shell=True)
                    stdout2 = p_cd_myhome.wait()
                    if stdout2 == 0:
                        clone_path = username + "@" + gitserver_ip + ":/home/" + username + "/" + bookname + ".git"
                        p = subprocess.Popen("cd " + myhome_path + ";git clone " + clone_path, shell=True)
                        (stdoutput,erroutput) = p.communicate()
                        # repo = Repo.init('/home/lidaxiang/' + bookname)
                        # repo.clone(clone_path)

                    return render(request, 'author/createNewBook.html', context)
        except Exception as e:
            context['mes_success'] = e
            # data['status'] = 'fail'
            # return render(request, 'reader/login.html')
            return render(request, 'author/createNewBook.html', context)

        # return render(request, 'result.html', context)
        # return render(request, 'author/createNewBook.html')
    else:
        return render(request, 'reader/login.html')

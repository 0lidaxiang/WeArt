# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
import subprocess
import paramiko
import sys
from git import Repo
import json

def index(request):
    context	= {}
    context['homepage'] = 'WeArt'
    context['classification'] = [{'val':"玄幻"},{'val':"都市"},{'val':"仙侠"}]
    context['contact'] = '联系我们'
    context['athlete_list'] = [{'val':1111},{'val':2222},{'val':333}]
    return render(request, 'hello.html', context)

def creategitrepository(request):
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

                return render(request, 'result.html', context)
    except Exception as e:
        context['mes_success'] = e
        return render(request, 'result.html', context)

def createNewChapter(request):
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    context = {}
    # get new book name and create respository in remote server
    # request.encoding='utf-8'
    context['mes_success'] = "success"
    context['bookname'] =  "You are updating book: " + request.GET['bookname'] + ","
    context['newChapter'] = "You are creating this book's chapter : " + request.GET['newChapter']

    loginId = "lidaxiang"
    cmd1 = "cd /home/" + loginId
    cmd2 = ";cd " + request.GET['bookname']
    cmd3 = ";touch " + request.GET['newChapter'] + ".txt"
    cmd = cmd1 + cmd2 + cmd3
    p = subprocess.Popen(cmd, shell=True)
    # next we should update to git server by git command but this is no need in test
    return render(request, 'result.html', context)

def updateContent(request):
    reload(sys)
    sys.setdefaultencoding('utf8')
    context = {}
    # get new book name and create respository in remote server
    request.encoding='utf-8'
    context['mes_success'] = "success"
    context['bookname'] =  "You are updating book: " + request.GET['bookname'] + ","
    context['newChapter'] = "You are updating this book's chapter : " + request.GET['chapterName']
    context['content'] = request.GET['content']

    loginId = "lidaxiang"

    filePath = "/home/" + loginId + "/" + request.GET['bookname'] + "/" + request.GET['chapterName'] + ".txt"
    f = open(filePath, "w")
    f.write(request.GET['content'] + "\n")
    f.close()

    myhome_path = "/home/" + loginId + "/" + request.GET['bookname']
    cmd1 = "cd " + myhome_path
    cmd2 = "; git config --global user.email user1@gmail.com; git config --global user.name user1"
    cmd = cmd1 + cmd2
    p = subprocess.Popen(cmd, shell=True)
    (stdoutput,erroutput) = p.communicate()

    # 新建版本库对象
    repo = Repo("/home/" + loginId + "/" + request.GET['bookname'])
    # 获取版本库暂存区
    index = repo.index
    # 添加修改文件
    index.add([request.GET['chapterName'] + '.txt'])
    # 提交修改到本地仓库
    index.commit(request.GET['commitContent'])

    # git = repo.git
    # git.add("chap1.txt") # git add test1.txt
    # #
    # git.commit('-m',  "'" + request.GET['commitContent']+"'")
    # git.commit('--amend', '--author="lidaxiang1 <lidaxiang@address.com>"' )



    # 获取远程仓库
    remote = repo.remote()
    origin = repo.remotes.origin
    # 推送本地修改到远程仓库
    origin.push()

    return render(request, 'result.html', context)

def getContentFromServer(request):
    bookname = request.POST['bookname'];
    chaptername = request.POST['chaptername'];

    loginId = "lidaxiang"

    cmd1 = "cd " + "/home/" + loginId + "/" + bookname
    cmd2= ";cat " + chaptername + ".txt"
    cmd = cmd1 + cmd2
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    content = list(p.stdout.readlines())
    contentList = []
    for v in content:
        contentList.append(v)

    return HttpResponse(json.dumps(contentList), content_type="application/json")

def showHistory(request):
        context = {}

        context['mes_success'] = "success"
        context['bookname'] =  "You are updating book: " + request.GET["bookname"] + ","

        loginId = "lidaxiang"


        cmd1 = "cd " + "/home/" + loginId + "/" + request.GET["bookname"]
        cmd2= ";git log"
        cmd = cmd1 + cmd2
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        logs = list(p.stdout.readlines())
        contentLog = []
        # tempstr = ""
        is_author = False
        for v in logs:
            if v.find(request.GET['author']) > -1 :
                is_author = True
            if is_author and v.startswith('commit'):
                contentLog.append(v.lstrip('commit') )

        context['logs'] = contentLog


        contenthistory = []
        contentLog.reverse()
        for logV in contentLog:
            cmd1 = "cd " + "/home/" + loginId + "/" + request.GET["bookname"]
            cmd2= ";git show " + logV
            cmd = cmd1 + cmd2
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            lp = list(p.stdout.readlines())

            flag = False
            for v in lp:
                if v.startswith('@@'):
                    flag = True
                    continue
                if flag == True and v.startswith("+") == True:
                    contenthistory.append(v.lstrip('+'))
                if flag == True and v.startswith("-") == True:
                    contenthistory.remove(v.lstrip('-'))
        context['history'] = contenthistory


        return render(request, 'result.html', context)

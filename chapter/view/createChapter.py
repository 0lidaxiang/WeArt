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

def createChapter(request):
    context = {}
    if "readerId" in request.session:
        if request.session["authorStatus"] == "active":
            reload(sys)
            sys.setdefaultencoding('utf8')

            readerId = request.session["readerId"]
            loginId = "lidaxiang"

            webServerHomeDir = "/home/" + loginId

            # get new book name and create respository in remote server
            request.encoding='utf-8'
            bookName = ""

            try:
                if 'bookName' in request.GET:
                    userInputBookName = request.GET['bookName']

                    if userInputBookName == "":
                        context['status'] = "fail"
                        context['message'] = "您還沒有填寫新書名稱。請重載後重新嘗試。"
                    else:
                        if 'chapterName' in request.GET:
                            userInputChapterName = request.GET['chapterName']

                            if userInputChapterName == "":
                                context['status'] = "fail"
                                context['message'] = "The chapter name is null."
                            else:
                                authorId = request.session['authorId']
                                bookName = authorId + "_" + userInputBookName

                                # step1: struct the chapter file name
                                # bookName_number_chapterName
                                # now = datetime.datetime.now()
                                # monthClassedDirName = "/home/" + gitserver_user + "/" + str(now.year) + "/" + str(now.month)
                                # localMonthClassedDir= webServerHomeDir + "/" + str(now.year) + "/" + str(now.month)
                                #
                                # res,mes = touchChapterFile(webServerHomeDir)
                                # if res:
                                #     pass
                                # else:
                                #     context['status'] = "fail"
                                #     context['message'] = mes
                                return JsonResponse(context)
                        else:
                            context['status'] = "fail"
                            context['message'] = "The chapterName variable is not in request.GET."
                else:
                    context['status'] = "fail"
                    context['message'] = "The bookName variable is not in request.GET."
            except Exception as e:
                        context['status'] = "fail"
                        context['message'] = str(e)
            return JsonResponse(context)
        else:
            return render(request, 'author/authorStatus/')
    else:
        return render(request, 'reader/login.html')

def touchChapterFile(operateDir):
    script_mkdir = settings.SCRIPT_MKDIR
    try:
        # cmd = "git config --global user.email user1@gmail.com; git config --global user.name user1"
        cmd = "cd " + operateDir + ";python " + script_mkdir
        p = subprocess.Popen(cmd, shell=True)
        (stdoutput,erroutput) = p.communicate()
        return True,""
    except Exception as e:
        return False,str(e)

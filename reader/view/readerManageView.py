#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# this must be not commented when develop finished
# @login_required(login_url='/reader/login')
def readerIndex(request):
    return render(request, 'reader/readerIndex.html')

# this must be not commented when develop finished
# @login_required(login_url='/reader/login')
def booksRecorded(request):
    return render(request, 'reader/booksRecorded.html')

# this must be not commented when develop finished
# @login_required(login_url='/reader/login')
def readingHistory(request):
    return render(request, 'reader/readingHistory.html')

# this must be not commented when develop finished
# @login_required(login_url='/reader/login')
def readerSetting(request):
    return render(request, 'reader/readerSetting.html')

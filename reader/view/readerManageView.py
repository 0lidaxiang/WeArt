#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render

# Create your views here.
def readerManageIndex(request):
    return render(request, 'reader/readerManage.html')

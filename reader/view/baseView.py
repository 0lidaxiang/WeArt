#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render

# Create your views here.
def login(request):
    if "readerId" in request.session:
        return render(request, 'reader/readerIndex.html')
    else:
        return render(request, 'reader/login.html')
# def register(request):
#     return render(request, 'reader/register.html')
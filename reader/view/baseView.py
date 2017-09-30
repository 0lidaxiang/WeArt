#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def login(request):
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')
    else:
        return HttpResponseRedirect("/reader/index/")

#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.http import HttpResponse
import hashlib

def createId(length, str):
    str = str.encode('utf8')
    res = hashlib.sha384(str).hexdigest()
    return res[0:length]

# def createGitRepository(request):
#     pass

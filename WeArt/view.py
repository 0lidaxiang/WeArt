# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
# import subprocess
# import paramiko
# import sys
# from git import Repo
# import json

def index(request):
    context	= {}
    return render(request, 'index.html', context)

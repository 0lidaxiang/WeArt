# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
# import subprocess
# import paramiko
# import sys
# from git import Repo
# import json

def login(request):
    context	= {}
    context['athlete_list'] = [{'val':1111},{'val':2222},{'val':333}]
    return render(request, 'login.html', context)
def register(request):
    context	= {}
    context['homepage'] = 'WeArt'
    context['athlete_list'] = [{'val':1111},{'val':2222},{'val':333}]
    return render(request, 'register.html', context)

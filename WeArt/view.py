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
    context['homepage'] = 'WeArt'
    context['classification'] = [{'val':"玄幻"},{'val':"都市"},{'val':"仙侠"},{'val':"Sign up"},{'val':"Login in"},{'val':"Logout"}]
    context['contact'] = '联系我们'
    context['athlete_list'] = [{'val':1111},{'val':2222},{'val':333}]
    return render(request, 'index.html', context)

#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from home.view.indexView import  *

urlpatterns = [
    url('^index/$', index),
    # url('^index2/$', index2),
    url('^aboutUs/$', aboutUs)

]

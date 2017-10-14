#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WeArt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from home.view.indexView import *


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^$', index),
    url('^index/$', index),
    url('^home/', include('home.urls')),
    url('^reader/', include('reader.urls')),
    url('^author/', include('author.urls')),
    url('^chapter/', include('chapter.urls')),
    url('^book/', include('book.urls')),
    url('^content/', include('content.urls')),
    url('^collection/', include('collection.urls')),
    url('^voteChapter/', include('voteChapter.urls')),
]

admin.site.site_header = 'WeArt 後臺管理'
admin.site.site_title = 'WeArt 後臺管理'
admin.site.index_title = 'WeArt 後臺管理'
admin.site.index_template = 'admin/index.html'

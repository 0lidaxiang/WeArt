from django.conf.urls import include, url
from django.contrib import admin
from content.view.createContent import  *
from content.view.getContent import  *
from content.view.readerGetContent import  *


urlpatterns = [
    # url('^login/$', login),
    url('^createAContent/$', createAContent),
    url('^chapterContent/$', chapterContent),
    url('^authorGetContent/$', authorGetContent),
    url('^readerGetContent/$', readerGetContent),
]

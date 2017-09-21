from django.conf.urls import include, url
from django.contrib import admin
from chapter.view.createChapter import  *
from chapter.view.getChapter import  *

urlpatterns = [
    # url('^login/$', login),
    url('^createAChapter/$', createAChapter),
    url('^getChapter/$', getChapter),
    url('^bookChapter/$', bookChapter),
]

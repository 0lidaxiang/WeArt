from django.conf.urls import include, url
from django.contrib import admin
from chapter.view.createChapter import  *

urlpatterns = [
    # url('^login/$', login),
    url('^createAChapter/$', createAChapter),
]

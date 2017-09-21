from django.conf.urls import include, url
from django.contrib import admin
from home.view.indexView import  *

urlpatterns = [
    url('^index/$', index),
]

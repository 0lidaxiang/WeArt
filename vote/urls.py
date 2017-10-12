from django.conf.urls import include, url
from django.contrib import admin
from vote.view.chapterVersionVote import *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^chapterVersionVote/$', chapterVersionVote),
]

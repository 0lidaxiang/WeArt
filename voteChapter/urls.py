from django.conf.urls import include, url
from django.contrib import admin
from voteChapter.view.chapterVersionVote import *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^getRating/$', getRating),
    url('^chapterVersionVote/$', chapterVersionVote),
]

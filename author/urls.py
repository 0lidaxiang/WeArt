from django.conf.urls import include, url

from author.view.artsManageView import  *

urlpatterns = [
    url('^authorStatus/$', authorStatus),
    url('^artsManage/$', artsManage),
    url('^createNewBook/$', createNewBook),
    url('^createNewChapter/$', createNewChapter),
    url('^createNewContent/$', createNewContent),

]

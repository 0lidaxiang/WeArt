from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from reader.view.baseView import  *
from reader.view.loginView import  *
from reader.view.registerView import  *
from reader.view.readerManageView import  *
from reader.view.modifyReader import  *
from author.view.artsManageView import  *

urlpatterns = [
    url('^register/$', TemplateView.as_view(template_name="reader/register.html")),
    url('^testForPageCollection/$', TemplateView.as_view(template_name="reader/testForPageCollection.html")),

    url('^login/', login),
    url('^logout/$', logout),
    url('^loginReader/$', loginReader),
    url('^registerReader/', registerReader),
    url('^activate/(.+)/$', activeReader),
    url('^modifyReader/$', modifyReader),

    url('^index/', readerIndex),
    url('^booksRecorded/$', booksRecorded),
    url('^readerSetting/$', readerSetting),
    url('^getEnableAuthorStatus/$', getEnableAuthorStatus),
    url('^modifyAuthorStatus/$', modifyAuthorStatus),

]

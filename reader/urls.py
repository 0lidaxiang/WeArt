from django.conf.urls import include, url
from django.contrib import admin
from reader.view.baseView import  *
from reader.view.loginView import  *
from reader.view.registerView import  *
from reader.view.readerManageView import  *
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),

    # The following two urls are not required to be verifing login status.
    url('^register/$', TemplateView.as_view(template_name="reader/register.html")),
    url('^login/$', login),
    url('^logout/$', logout),
    url('^loginReader/$', loginReader),
    url('^registerReader/', registerReader),
    url('^activate/(.+)/$', activeReader),

    url('^index/', readerIndex),
    url('^booksRecorded/$', booksRecorded),
    url('^readingHistory/$', readingHistory),
    url('^readerSetting/$', readerSetting),
    url('^getEnableAuthorStatus/$', getEnableAuthorStatus),
    url('^modifyAuthorStatus/$', modifyAuthorStatus),
]
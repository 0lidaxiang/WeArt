from django.conf.urls import include, url
from django.contrib import admin
# from tool.tools import registerReader
# from tool.tools import active_user
from reader.view.baseView import  *
from reader.view.loginView import  *
from reader.view.registerView import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^login/$', login),
    url('^register/$', register),
    url('^loginReader/$', loginReader),
    url('^registerReader/', registerReader),
    url('^activate/(.+)/$', activeReader),
]

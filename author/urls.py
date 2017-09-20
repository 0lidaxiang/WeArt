from django.conf.urls import include, url

from author.view.artsManageView import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^authorStatus/$', authorStatus),
    url('^artsManage/$', artsManage),
    # url('^createABook/$', createABook),
    url('^createNewBook/$', createNewBook),
    url('^createNewChapter/$', createNewChapter),
    url('^createNewContent/$', createNewContent),

]

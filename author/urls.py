from django.conf.urls import include, url

from author.view.artsManageView import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),

    url('^artsManage/$', artsManage),
    url('^createNewBook/$', createNewBook),
    url('^createNewChapter/$', createNewChapter),
    url('^createNewContent/$', createNewContent),

]

from django.conf.urls import include, url

from book.view.createBook import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^createABook/$', createABook),
    # url('^createNewBook/$', createNewBook),
]

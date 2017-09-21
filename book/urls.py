from django.conf.urls import include, url

from book.view.createBook import  *
from book.view.getRecommendArts import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^createABook/$', createABook),
    # url('^createNewBook/$', createNewBook),
    url('^getRecommendArts/$', getRecommendArts),
]

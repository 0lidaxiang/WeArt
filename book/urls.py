from django.conf.urls import include, url

from book.view.createBook import  *
from book.view.getRecommendArts import  *
from book.view.deleteBook import  *
from book.view.getBook import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^createABook/$', createABook),
    url('^getMyBook/$', getMyBook),
    url('^deleteBook/$', deleteObj),
    url('^getRecommendArts/$', getRecommendArts),
]

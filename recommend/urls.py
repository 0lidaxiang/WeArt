from django.conf.urls import include, url

from recommend.view.getRecommendArts import  *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url('^getRecommendArts/$', getRecommendArts),
]

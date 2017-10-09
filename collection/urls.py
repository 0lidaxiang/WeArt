from django.conf.urls import include, url
from django.contrib import admin
from collection.view.baseView import *
from collection.view.addCollection import *
from collection.view.getCollection import *
from collection.view.deleteCollection import *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url('^$', index),
    url('^addCollectionInter/$', addCollectionInter),
    url('^addCollection/$', add),
    url('^goToAddCollection/$', goToAddCollection),
    url('^getMyCollection/$', getMyCollection),
    url('^delete/$', delete),
]

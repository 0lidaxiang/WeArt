from django.conf.urls import include, url
from django.views.generic import TemplateView
from author.view.artsManageView import  *

urlpatterns = [
    url('^authorStatus/$', authorStatus),
    url('^artsManage/$', artsManage),
    url('^createNewBook/$', createNewBook),
    url('^createNewChapter/$', createNewChapter),
    url('^createNewContent/$', createNewContent),
    url('^testForPageWriter/$', TemplateView.as_view(template_name="author/testForPageWriter.html")),
    url('^testForPageWriterWriting/$', TemplateView.as_view(template_name="author/testForPageWriterWriting.html")),
]

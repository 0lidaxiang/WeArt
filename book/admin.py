#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import strftime
from django.contrib import admin
from django.contrib.admin import AdminSite
from book.models import book
from django.utils.translation import ugettext_lazy as _

class bookAdmin(admin.ModelAdmin):
    # title = models.CharField("分类名称",max_length=100,db_index=True,unique=True)
    def get_queryset(self, request):
        qs = super(bookAdmin, self).get_queryset(request)
        self.qs = qs
        return qs
    def ids(self, obj):
        return len(self.qs) - list(self.qs).index(obj)
    ids.short_description = "順序"

    def modifyText(self, obj):
        return "修改"
    modifyText.short_description = "修改鏈接"

    list_max_show_all = 20
    list_display = ('ids', 'name', 'remoteIP', 'location', 'chapterCount', "idReader_id", 'status', 'accountCreateTime', "accountStatus", "modifyText")
    search_fields = ('name', 'idReader_id')
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ('id', 'remoteIP', 'location', 'chapterCount', "idReader_id", "createTime")
    list_display_links = ('ids', 'modifyText')
    view_on_site = True

    # forbid adding new object
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True  # forbid visiting object-list-page
        else:
            return True # forbid visiting change-object-page

# Register your models here.
admin.site.register(book, bookAdmin)

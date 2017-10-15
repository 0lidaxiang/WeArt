#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import strftime
from django.contrib import admin
from django.contrib.admin import AdminSite
from recommand.models import recommand
from django.utils.translation import ugettext_lazy as _

class recommandAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(recommandAdmin, self).get_queryset(request)
        self.qs = qs
        return qs
    def ids(self, obj):
        return len(self.qs) - list(self.qs).index(obj)
    ids.short_description = "順序"

    def modifyText(self, obj):
        return "修改"
    modifyText.short_description = "修改鏈接"

    list_max_show_all = 20
    list_display = ('ids', 'idBook_id', 'status', "accountStatus", "createTime", "modifyTime", "modifyText")
    search_fields = ('idBook_id', 'status')
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ('id', "createTime", "modifyTime")
    list_display_links = ('ids', 'modifyText')
    view_on_site = True

    # allowed adding new object
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True  # allow visiting object-list-page
        else:
            return True # allow visiting change-object-page
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True  # allow visiting object-list-page
        else:
            return True # allow visiting delete-object-page

# Register your models here.
admin.site.register(recommand, recommandAdmin)

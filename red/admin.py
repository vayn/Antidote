#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: admin.py
# @Date: 2011年03月09日 星期三 23时49分38秒

from django.contrib import admin
from antidote.red.models import Tag, Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'tags_inline')
    search_fields = ('title',)
    date_hierarchy = 'pub_date'
    filter_horizontal = ('tags',)

admin.site.register(Tag)
admin.site.register(Entry, EntryAdmin)

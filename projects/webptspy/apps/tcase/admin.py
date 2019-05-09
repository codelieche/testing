# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Case, Execute, Shiwu

# Register your models here.


class CaseModelAdmin(admin.ModelAdmin):
    """
    Case Model Admin
    """
    list_display = ('id', 'name', 'project', 'add_time')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'project')
    list_filter = ('add_time',)
    ordering = ('id',)


class ExecuteModelAdmin(admin.ModelAdmin):
    """
    Execute Model Admin
    """
    list_display = ('id', 'name', 'case', 'user', 'status', 'port',
                    'time_start', 'time_end')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'case')
    list_filter = ('case', 'status', 'user')
    ordering = ('id',)


class ShiwuModelAdmin(admin.ModelAdmin):
    """
    Shiwu Model Admin
    """
    list_display = ('id', 'name', 'project', 'user', 'method', 'url',
                    'is_startup', 'body', 'cycle')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('project', 'method', 'is_startup', 'cycle')
    ordering = ('id',)

admin.site.register(Case, CaseModelAdmin)
admin.site.register(Execute, ExecuteModelAdmin)
admin.site.register(Shiwu, ShiwuModelAdmin)

# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import Project

# Register your models here.


class ProjectModelAdmin(admin.ModelAdmin):
    """
    Project Model Admin
    """
    list_display = ('id', 'name_en', 'name', 'address', 'address_pro',
                    'need_test')
    list_display_links = ('name_en',)
    search_fields = ('name', 'name_en', 'address', 'address_pro')
    list_filter = ('need_test',)
    ordering = ('id',)

admin.site.register(Project, ProjectModelAdmin)

# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import Summary, StatsCSV, Detail
# Register your models here.


class SummaryModelAdmin(admin.ModelAdmin):
    """
    执行摘要管理Model
    """
    list_display = ('id', 'execute', 'user_count', 'total_rps', 'add_time')
    list_display_links = ('execute',)
    list_filter = ('execute', 'total_rps', 'add_time')
    search_fields = ('execute',)


class StatsCSVModelAdmin(admin.ModelAdmin):
    """
    统计信息管理Model
    """
    list_display = ('id', 'execute', 'csv_type', 'add_time')
    list_filter = ('execute', 'csv_type', 'add_time')
    search_fields = ('execute',)

admin.site.register(Summary, SummaryModelAdmin)
admin.site.register(StatsCSV, StatsCSVModelAdmin)
admin.site.register(Detail)

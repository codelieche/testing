# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileModelAdmin(admin.ModelAdmin):
    """
    用户管理Model
    """
    list_display = ('id', 'username', 'nike_name', 'mobile',
                    'email', 'is_active')
    list_filter = ('is_active',)
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email', 'mobile', 'nike_name')

admin.site.register(UserProfile, UserProfileModelAdmin)

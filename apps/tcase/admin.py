# _*_ coding:utf-8 _*_
from django.contrib import admin
from .models import Case, CaseCode, Execute

# Register your models here.

admin.site.register(Case)
admin.site.register(CaseCode)
admin.site.register(Execute)


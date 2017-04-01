# -*- coding:utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Project(models.Model):
    """
    项目Model
    """
    name = models.CharField(max_length=64, verbose_name="项目")
    name_en = models.CharField(max_length=64, verbose_name="英文简称")
    principal = models.CharField(max_length=64, verbose_name="负责人")
    address = models.CharField(max_length=128, verbose_name="测试地址",
                               blank=True)
    address_pro = models.CharField(max_length=100, verbose_name="生产地址",
                                   blank=True, null=True)
    jira_key = models.CharField(max_length=64, verbose_name="jira_key",
                                blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name

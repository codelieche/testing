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
    need_test = models.BooleanField(default=True, verbose_name="是否需要测试")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class ServerInfo(models.Model):
    """
    项目服务信息Model
    数据库：正式数据库，测试数据库: test_db, product_db
    项目发布：k8s pod方式：test_deployment, product_deployment
    项目发布：物理服务器：test_server, product_server
    """
    project = models.OneToOneField(to=Project, verbose_name="项目")
    # 数据库信息
    test_db = models.CharField(max_length=100, verbose_name="测试数据库",
                               blank=True, null=True)
    product_db = models.CharField(max_length=100, verbose_name="正式数据库",
                                  blank=True, null=True)

    # k8s pod部署
    test_deployment = models.CharField(max_length=100, verbose_name="测试Pod",
                                       blank=True, null=True)
    product_deployment = models.CharField(max_length=100, verbose_name="正式Pod",
                                          blank=True, null=True)

    # 物理服务器部署
    test_server = models.CharField(max_length=100, verbose_name="测试Server",
                                   blank=True, null=True)
    product_server = models.CharField(max_length=100, verbose_name="正式Server",
                                      blank=True, null=True)

    def __str__(self):
        return "{} server info".format(self.project)

    class Meta:
        verbose_name = "项目服务信息"
        verbose_name_plural = verbose_name

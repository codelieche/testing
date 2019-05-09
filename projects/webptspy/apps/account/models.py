# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class UserProfile(AbstractUser):
    """
    用户信息Model
    """
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密'),
    )

    nike_name = models.CharField(max_length=40, blank=True, verbose_name="昵称")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              verbose_name="性别", default="secret")
    mobile = models.CharField(max_length=11, verbose_name="手机号", blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

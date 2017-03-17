# _*_ coding:utf-8 _*_
"""
自定义用户验证
"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 用户有可能传入的是邮箱或者用户名
            # 用Q来让查询条件实现或的功能
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username)
            )
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return Nonepy
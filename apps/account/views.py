# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

# Create your views here.


class LoginView(View):
    """
    用户登录View
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # 登录后跳转到next
                next_url = request.GET.get('next', '/')
                return redirect(to=next_url)
            else:
                return render(request, 'account/login.html', {
                    'info': '用户名或密码错误',
                    'form': form
                })
        else:
            return render(request, 'account/login.html', {
                'info': '用户名或密码不合法',
                'form': form
            })


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        next_url = request.GET.get('next', '/')
        return redirect(next_url)


def page_403(request):
    return render(request, '403.html')


def page_404(request):
    return render(request, '404.html')


def page_500(request):
    return render(request, '500.html')

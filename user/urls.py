#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    # 用户的注册和登录
    path('login.html', views.login_view, name='login_view'),
    # 用户中心
    path('home/<int:page>.html', views.home_view, name='home_view'),
    # 退出用户登录
    path('logout.html', views.logout_view, name='logout_view'),
]


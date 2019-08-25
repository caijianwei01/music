#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index_view, name='index_view'),
]


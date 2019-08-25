#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('<int:page>.html', views.search_view, name='search_view'),
]


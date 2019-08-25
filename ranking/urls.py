#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

app_name = 'ranking'
urlpatterns = [
    path('', views.ranking_view, name='ranking_view'),
]


#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('<int:song_id>.html', views.comment_view, name='comment_view'),
]


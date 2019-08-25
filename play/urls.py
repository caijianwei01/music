#!/usr/bin/env python
# encoding: utf-8
from django.urls import path
from . import views

app_name = 'play'
urlpatterns = [
    # 歌曲播放页面
    path('<int:song_id>.html', views.play_view, name='play_view'),
    # 歌曲下载
    path('download/<int:song_id>.html', views.download_view, name='download'),
]


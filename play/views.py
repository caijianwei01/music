#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render
from django.http import FileResponse
from django.utils.http import urlquote
from myutils import myutil
from index.models import *


# Create your views here.
# 歌曲播放首页
def play_view(request, song_id):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 播放列表
    play_list = request.session.get('play_list', [])
    song_exist = False
    if play_list:
        for i in play_list:
            if int(song_id) == i['song_id']:
                song_exist = True
    if song_exist == False:
        play_list.append({
            'song_id': int(song_id),
            'song_singer': song_info.song_singer,
            'song_name': song_info.song_name,
            'song_time': song_info.song_time
        })
    request.session['play_list'] = play_list
    # 歌词
    if song_info.song_lyrics != '暂无歌词':
        with open('static/songLyric/' + song_info.song_lyrics, 'r', encoding='utf-8') as f:
            song_lyrics = f.read()
    # 相关歌曲
    song_type = Song.objects.values('song_type').get(song_id=song_id)['song_type']
    song_relevant = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by(
        '-dynamic_play').all()[:6]
    # 添加播放次数
    # 扩展功能：可使用session实现每天只添加一次播放次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来的基础上加1
    if dynamic_info:
        dynamic_info.dynamic_play += 1
        dynamic_info.save()
    else:
        # 若动态信息不存在，则创建新的动态信息
        dynamic_info = Dynamic(dynamic_play=1, dynamic_search=0, dynamic_down=0, song_id=song_id)
        dynamic_info.save()
    return render(request, 'play/play.html', locals())


# 歌曲下载
def download_view(request, song_id):
    # 根据song_id查找歌曲信息, first()用于返回第一个结果
    song_info = Song.objects.filter(song_id=int(song_id)).first()
    # 根据song_id获取歌曲动态信息表，添加下载次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来的基础上加1
    if dynamic_info:
        dynamic_info.dynamic_down += 1
        dynamic_info.save()
    else:
        # 若动态信息不存在，则创建新的动态信息
        dynamic_info = Dynamic(dynamic_play=0, dynamic_search=0, dynamic_down=1, song_id=int(song_id))
        dynamic_info.save()
    # 将读取的歌曲文件内容写入StreamingHttpResponse对象，并以字节流的方式返回给用户
    file = 'static/songFile/' + song_info.song_file
    filename = song_info.song_name + '.mp3'
    response = FileResponse(myutil.file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    # 下载中文文件名文件：使用urlquote()函数处理文件名，始之支持中文显示
    # response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf-8').decode('ISO-8859-1'))
    response['Content-Disposition'] = 'attachment; filename={0}'.format(urlquote(filename))
    return response

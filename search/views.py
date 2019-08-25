from django.shortcuts import render, redirect
from django.db.models import Q
from myutils import myutil
from index.models import *


# Create your views here.

# 歌曲搜索
def search_view(request, page):
    if request.method == 'GET':
        # 搜索歌曲
        search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
        # 获取搜索内容， 如果kword为空就查询全部歌曲
        kword = request.session.get('kword', '')
        if kword:
            # Q 是SQL语句里的or语法
            song_info = Song.objects.values('song_id', 'song_name', 'song_singer', 'song_time').filter(
                Q(song_name__icontains=kword) | Q(song_singer=kword)).order_by('-song_release').all()
        else:
            song_info = Song.objects.values('song_id', 'song_name', 'song_singer', 'song_time').order_by(
                '-song_release').all()
        # 分页功能,每页显示的数量6
        page_count = 13
        contacts = myutil.pagination(song_info, page_count, page)
        # 添加歌曲搜索次数
        song_exist = Song.objects.filter(Q(song_name__icontains=kword) | Q(song_singer=kword)).all()
        if song_exist:
            for song in song_exist:
                song_id = song.song_id
                dynamic_info = Dynamic.objects.filter(song_id=song_id).first()
                # 判断歌曲动态信息是否存在，存在就在原来的基础上加1
                if dynamic_info:
                    dynamic_info.dynamic_search += 1
                    dynamic_info.save()
                else:
                    # 若动态信息不存在，则创建新的动态信息
                    dynamic = Dynamic(dynamic_down=0, dynamic_play=0, dynamic_search=1, song_id=song_id)
                    dynamic.save()
        return render(request, 'search/search.html', locals())
    else:
        # 处理POST请求，并重定向搜索页面
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('%d.html' % page)

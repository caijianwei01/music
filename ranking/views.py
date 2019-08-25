from django.shortcuts import render
from index.models import *
from myutils import myutil
import re


# Create your views here.

# 歌曲排行
def ranking_view(request):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 歌曲分类列表
    type_list = Song.objects.values('song_type').distinct()
    # 歌曲列表信息
    song_type = request.GET.get('type', '')
    # 获取label_id的值
    label_id = request.GET.get('label_id', '')
    # 页数
    page = request.GET.get('page', '')
    # 对获取的page值类似page='2?label_id=2'进行特殊处理
    if '?' in page:
        # 对page值进行分割，用？、=进行分割
        page_list = re.split(r'[\?\=]', page)
        if 'label_id' in page:
            page = page_list[0]
            label_id = page_list[2]
        elif 'type' in page:
            page = page_list[0]
            song_type = page_list[2]
    # 每页显示的数量
    page_count = 9
    if song_type:
        # ‘-xxx’：根据xxx字段降序排列
        song_info = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by(
            '-dynamic_play').all()
    elif label_id:
        song_info = Dynamic.objects.select_related('song').filter(song__label_id=label_id).order_by(
            '-dynamic_play').all()
    else:
        song_info = Dynamic.objects.select_related('song').order_by('-dynamic_play').all()
    # 分页设置
    page_info = myutil.pagination(song_info, page_count, page)
    return render(request, 'ranking/ranking.html', locals())

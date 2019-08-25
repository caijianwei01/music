from django.shortcuts import render, redirect
from user.models import *
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from .form import MyUserCreationForm
from django.contrib.auth.decorators import login_required
from myutils import myutil
from index.models import *


# Create your views here.
# 用户注册和登录
def login_view(request):
    # 表单对象
    user = MyUserCreationForm()
    # 表单提交
    if request.method == 'POST':
        # 判断表单提交是用户登录还是注册
        # 用户登录
        if request.POST.get('loginUser', ''):
            loginUser = request.POST.get('loginUser', '')
            password = request.POST.get('password', '')
            if MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)):
                user = MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)).first()
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('home/1.html')
                else:
                    error_tips = '密码错误'
            else:
                error_tips = '用户不存在'
        else:
            # 用户注册
            user = MyUserCreationForm(request.POST)
            if user.is_valid():
                user.save()
                tips = '注册成功'
            else:
                if user.errors.get('username', ''):
                    error_tips = user.errors.get('username', '注册失败')
                else:
                    error_tips = user.errors.get('mobile', '注册失败')
    return render(request, 'user/login.html', locals())


# 用户中心
# 设置用户登录权限
@login_required(login_url='/user/login.html')
def home_view(request, page):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 分页功能
    song_info = request.session.get('play_list', [])
    page_count = 6
    contacts = myutil.pagination(song_info, page_count, page)
    return render(request, 'user/home.html', locals())


# 退出登录
def logout_view(request):
    logout(request)
    return redirect('/')

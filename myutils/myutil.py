#!/usr/bin/env python
# encoding: utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 读取文件内容,默认每次读取512字节的内容
def file_iterator(file, chunk_size=1024):
    with open(file, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# 分页
def pagination(pag_list, pag_count, page):
    # 设置每页的数据量
    page_list = Paginator(pag_list, pag_count)
    try:
        # 根据传进来的页数返回分页数据
        page_info = page_list.page(page)
    except PageNotAnInteger:
        # 如果参数page的数据类型不是整形，就返回第一页数据
        page_info = page_list.page(1)
    except EmptyPage:
        # 如果用户访问的页数大于实际页数，则放回最后一页的数据
        page_info = page_list.page(page_list.num_pages)
    return page_info

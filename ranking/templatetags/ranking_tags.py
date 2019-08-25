#!/usr/bin/env python
# encoding: utf-8
from django import template

register = template.Library()


@register.filter
def multiply(value, num):
    # 定义一个乘法过滤器
    return (value - 1) * num

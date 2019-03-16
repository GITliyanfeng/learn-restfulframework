# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 15:44
# @Author  : __Yanfeng
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from myweb import views

urlpatterns = [
    url(r'^code/$', views.code_list, name='codeList'),
    url(r'^code/(?P<pk>[0-9]+)/$', views.code_detail, name='codeDetail'),
]

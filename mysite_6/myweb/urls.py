# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 15:44
# @Author  : __Yanfeng
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from myweb import views
# 导入请求的时候指定数据类型
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^code/$', views.CodeList.as_view(), name='codesegment-list'),
    url(r'^code/(?P<pk>[0-9]+)/$', views.CodeDetaile.as_view(), name='codesegment-detail'),
    url(r'^code/(?P<pk>[0-9]+)/highlighted/$', views.CodeHighlight.as_view(), name='codesegment-highlight'),
    url(r'^user/$', views.UserList.as_view(), name='user-list'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetaile.as_view(), name='user-detail'),
]

# 对原有的urlpatterns进行格式化
urlpatterns = format_suffix_patterns(urlpatterns)

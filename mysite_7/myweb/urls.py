# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 15:44
# @Author  : __Yanfeng
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from myweb.views import api_root, CodeSegmentViewSet, UserViewSet
# 导入请求的时候指定数据类型
from rest_framework.urlpatterns import format_suffix_patterns

# 载入渲染器
from rest_framework import renderers

# 手动编辑as_view的动作
# 传入的参数是一个字典,键---->请求方式  值---->对应的动作
CodeList = CodeSegmentViewSet.as_view(
    {
        'get': 'list',
        'post': 'create'
    },
)
CodeDetaile = CodeSegmentViewSet.as_view(
    {
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }
)
CodeHighlight = CodeSegmentViewSet.as_view(
    {
        'get': 'highlight',
    }, renderer_classes=[renderers.StaticHTMLRenderer]  # 自定义动作需要传入的参数
)
UserList = UserViewSet.as_view(
    {
        'get': 'list',
    }
)
UserDetaile = UserViewSet.as_view(
    {
        'get': 'retrieve',
    }
)
urlpatterns = [
    url(r'^$', api_root),
    url(r'^code/$', CodeList, name='codesegment-list'),
    url(r'^code/(?P<pk>[0-9]+)/$', CodeDetaile, name='codesegment-detail'),
    url(r'^code/(?P<pk>[0-9]+)/highlighted/$', CodeHighlight, name='codesegment-highlight'),
    url(r'^user/$', UserList, name='user-list'),
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetaile, name='user-detail'),
]

# 对原有的urlpatterns进行格式化
urlpatterns = format_suffix_patterns(urlpatterns)

# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 0022 15:35
# @Author  : __Yanfeng
# @Site    : 
# @File    : permissions.py
# @Software: PyCharm


######
#
# 自定义权限
#
######

from  rest_framework import permissions


# 检测是否是该对象的拥有着,否则只读,继承与permissions.BasePermission
class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
        为了使每一个CodeSegment对象只能让他的拥有着去修改它
    '''
    def has_object_permission(self, request, view, obj):
        # 任何游客都可以对齐访问,只是仅仅owner能修改,所以GET，HEAD，OPTIONS请求都属于安全请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 当请求不再是上面的安全请求,就需要判断当前用户是否是CodeSegment对象的拥有者,一致允许,不一致返回错误信息
        return obj.owner == request.user

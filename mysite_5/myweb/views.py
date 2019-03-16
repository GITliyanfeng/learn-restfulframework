from django.shortcuts import render
# CodeSegment 序列化
from myweb.models import CodeSegment
from myweb.serializers import CodeSegmentSerializers
# 使用generics类来更加简化代码
from rest_framework import generics
# User 序列化
from django.contrib.auth.models import User
from myweb.serializers import UserSerializers
from rest_framework import permissions  # 导入权限管理
from myweb.permissions import IsOwnerOrReadOnly # 导入自定义权限

# Create your views here.

class CodeList(
    generics.ListCreateAPIView,  #
):
    # 模型对象
    queryset = CodeSegment.objects.all()
    # 所使用的序列化控制器
    serializer_class = CodeSegmentSerializers
    # 权限判断  是否是创建者,否则只读
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CodeDetaile(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = CodeSegment.objects.all()
    serializer_class = CodeSegmentSerializers
    # 两个参数都是指定单查询依据的字段,如果定义lookup_url_kwarg,会使用这个,如果未定义,则使用lookup_field,默认为'pk'
    lookup_field = 'title'
    # lookup_url_kwarg = 'title'
    # 权限判断
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserDetaile(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

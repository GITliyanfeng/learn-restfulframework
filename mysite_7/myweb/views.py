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
from myweb.permissions import IsOwnerOrReadOnly  # 导入自定义权限

# 使用ViewSet让代码更加的简便
from rest_framework import viewsets
from rest_framework.decorators import detail_route # 创建自定义动作的装饰器

# 装饰器方式渲染跟路由
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# 渲染器
from rest_framework import renderers


# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': reverse(viewname='user-list', request=request, format=format),
            'codes': reverse(viewname='codesegment-list', request=request, format=format),
        }
    )


# 使用ReadOnlyModelViewSet是因为User模型对于前台来说是只读的
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        在viewsets中,已经打包实现了  list 和 detail 的动作
        所以可以以将UserList以及UserDetail两个类集合在一起
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializers


class CodeSegmentViewSet(viewsets.ModelViewSet):
    '''
        ModelViewSet实现了`list`, `create`, `retrieve`,
    `update` 和 `destroy` 动作.

    同时我们手动增加一个额外的'highlight'动作用于查看高亮的代码段

    '''
    queryset = CodeSegment.objects.all()
    serializer_class = CodeSegmentSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    # 创建自定义的动作  highlight
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        codesegment = self.get_object()
        return Response(codesegment.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CodeList(
    generics.ListCreateAPIView,  #
):
    # 模型对象
    queryset = CodeSegment.objects.all()
    # 所使用的序列化控制器
    serializer_class = CodeSegmentSerializers
    # 权限判断  是否是创建者,否则只读
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 登陆的时候会自动将用户id存入request,所以需要通过request来获取当前用户
    # 在创建新的CodeSegment对象的时候将对象的owner字段设置为self.request.user
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CodeDetaile(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = CodeSegment.objects.all()
    serializer_class = CodeSegmentSerializers
    # 两个参数都是指定单查询依据的字段,如果定义lookup_url_kwarg,会使用这个,如果未定义,则使用lookup_field,默认为'pk'
    # lookup_field = 'title'
    # lookup_url_kwarg = 'title'
    # 权限判断
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserDetaile(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class CodeHighlight(generics.GenericAPIView):
    queryset = CodeSegment.objects.all()
    # 加载静态HTML渲染器
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        code = self.get_object()
        return Response(code.highlighted)

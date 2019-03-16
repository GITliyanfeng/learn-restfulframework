from django.shortcuts import render
from myweb.models import CodeSegment
from myweb.serializers import CodeSegmentSerializers
# 使用mixins类来简化代码
from rest_framework import mixins
from rest_framework import generics


# Create your views here.

class CodeList(
    mixins.ListModelMixin,  # 实现list 亲求数据列表显示的方法
    mixins.CreateModelMixin,  # 实现 创建数据的方法
    generics.GenericAPIView,  #
):
    # 模型对象
    queryset = CodeSegment.objects.all()
    # 所使用的序列化控制器
    serializer_class = CodeSegmentSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, requset, *args, **kwargs):
        return self.create(requset, *args, **kwargs)


class CodeDetaile(
    mixins.RetrieveModelMixin,  # 单对像检索
    mixins.UpdateModelMixin,  # 更新对像
    mixins.DestroyModelMixin,  # 删除对象
    generics.GenericAPIView,
):
    queryset = CodeSegment.objects.all()
    serializer_class = CodeSegmentSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

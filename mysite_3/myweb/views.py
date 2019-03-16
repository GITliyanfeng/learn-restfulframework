from django.shortcuts import render
# csrf_exempt 取消csrf验证的装饰器
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from myweb.models import CodeSegment
from myweb.serializers import CodeSegmentSerializers
# 使用APIView类
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class CodeList(APIView):
    def get(self, request, format=None):
        codes = CodeSegment.objects.all()
        serializer = CodeSegmentSerializers(codes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CodeSegmentSerializers(data=request.data)
        if serializer.is_valid():
            # 如果验证通过的话,执行save()将反序列化的数据储存到数据库
            serializer.save()
            # 返回序列化的数据,以及201创建成功状态码
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # 如果验证失败,返回错误信息,以及400错误状态码
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeDetaile(APIView):
    def get_object(self, pk):
        try:
            code = CodeSegment.objects.get(pk=pk)
        except CodeSegment.DoesNotExist:
            raise Http404

    def get(self, request, pk, fromat=None):
        code = self.get_object(pk)
        serializer = CodeSegmentSerializers(code)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        code = self.get_object(pk)
        serializer = CodeSegmentSerializers(code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # 验证错误后返回400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        code = self.get_object(pk)
        code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

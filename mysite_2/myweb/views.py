from django.shortcuts import render
# csrf_exempt 取消csrf验证的装饰器
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from myweb.models import CodeSegment
from myweb.serializers import CodeSegmentSerializers
# 使用api装饰器
from rest_framework import status  # 拓展之后的状态码
from rest_framework.decorators import api_view  # api_view 装饰器
from rest_framework.response import Response  # 拓展之后的响应对象


# Create your views here.

@api_view(['GET', 'POST'])
def code_list(request, format=None):
    '''
    通过区分GET/POST请求方式,获取所有的CodeSegment对象
    或者创建一个新的CodeSegment对象
    :param request:请求上下文
    :return:
    '''
    # GET 获取
    if request.method == 'GET':
        # 获取models对象
        codes = CodeSegment.objects.all()
        # 将对对象传入控制器类,生成控制器
        serializer = CodeSegmentSerializers(codes, many=True)
        # 返回控制器序列化的data
        return Response(serializer.data)
        # POST 创建
    elif request.method == 'POST':
        # 从请求上下文中获取数据,将数据解析为反序列化的数据
        # 将序列化的数据传给控制器类,生成新的控制器
        serializer = CodeSegmentSerializers(data=request.data)
        # 判断新控制器中的数据是否能够被验证通过
        if serializer.is_valid():
            # 如果验证通过的话,执行save()将反序列化的数据储存到数据库
            serializer.save()
            # 返回序列化的数据,以及201创建成功状态码
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 如果验证失败,返回错误信息,以及400错误状态码
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def code_detail(request, pk, format=None):
    '''
    针对单个对象
    GET     获取
    PUT     更新
    DELETE  删除
    :param request:
    :param pk: 主键,或者其他唯一标识
    :return:
    '''
    # 首先根据主键获取单个code对象
    try:
        code = CodeSegment.objects.get(pk=pk)
    except CodeSegment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # 将对象传入控制器,铜鼓控制器序列化
        serializer = CodeSegmentSerializers(code)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 从request中获取数据,通过控制器,传入旧的code对象,以及反序列化后的新data
        serializer = CodeSegmentSerializers(code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # 验证错误后返回400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # delete请求要删除对象,执行对象的删除方法,返回204删除成功的状态码
        code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# csrf_exempt 取消csrf验证的装饰器
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from myweb.models import CodeSegment
from myweb.serializers import CodeSegmentSerializers


# Create your views here.


def code_list(request):
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
        return JsonResponse(serializer.data, safe=False)
        # POST 创建
    elif request.method == 'POST':
        # 从请求上下文中获取数据,将数据解析为反序列化的数据
        data = JSONParser().parse(request)
        # 将序列化的数据传给控制器类,生成新的控制器
        serializer = CodeSegmentSerializers(data=data)
        # 判断新控制器中的数据是否能够被验证通过
        if serializer.is_valid():
            # 如果验证通过的话,执行save()将反序列化的数据储存到数据库
            serializer.save()
            # 返回序列化的数据,以及201创建成功状态码
            return JsonResponse(serializer.data, status=201)
        # 如果验证失败,返回错误信息,以及400错误状态码
        return JsonResponse(serializer.errors, status=400)


def code_detail(request, pk):
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
        return HttpResponse(status=404)

    if request.method == 'GET':
        # 将对象传入控制器,铜鼓控制器序列化
        serializer = CodeSegmentSerializers(code)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        # 从request中获取数据,通过控制器,传入旧的code对象,以及反序列化后的新data
        data = JSONParser().parse(request)
        serializer = CodeSegmentSerializers(code, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # 验证错误后返回400
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # delete请求要删除对象,执行对象的删除方法,返回204删除成功的状态码
        code.delete()
        return HttpResponse(status=204)

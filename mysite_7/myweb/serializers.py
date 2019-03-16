# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 11:30
# @Author  : __Yanfeng
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers
from myweb.models import CodeSegment, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class CodeSegmentSerializers_2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # 通过字控制序列化器渲染到html页面的时候显式的模板
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    # 给定经过验证的数据,创建并返回一个新的CodeSegment实例
    def create(self, validated_data):
        '''
        创建数据
        :param validated_data: 经过验证的数据
        :return: 返回一个models的实例
        '''
        return CodeSegment.objects.create(**validated_data)

    # 给定经过验证的数据,更新并返回一个已经存在的CodeSegment实例
    def update(self, instance, validated_data):
        '''
        更新数据
        :param instance: 要跟新的models实例
        :param validated_data: 经过验证的数据
        :return: 返回更新后的models实例
        '''
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# 通过模型的简化版本
class CodeSegmentSerializers(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='codesegment-highlight', format='html')

    class Meta:
        # 序列化控制器基于的模型
        model = CodeSegment
        fields = ('id', 'url', 'title', 'code', 'linenos', 'language', 'style', 'owner', 'highlight',)


# 用户模型序列化器

class UserSerializers(serializers.HyperlinkedModelSerializer):
    CodeSegments = serializers.HyperlinkedIdentityField(many=True, view_name='codesegment-detail')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'CodeSegments',)

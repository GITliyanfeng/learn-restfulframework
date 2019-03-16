from django.db import models
from pygments.lexers import get_all_lexers  # 导入获取编程语言
from pygments.styles import get_all_styles  # 导入获取配色分隔

# Create your models here.

# 获取 LEXERS (词法分析器)
LEXERS = [item for item in get_all_lexers() if item[1]]
# 通过词法分析器获取所有编程语言
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# 获取颜色风格列表
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class CodeSegment(models.Model):
    '''
    参数:
        blank  字段可以空白 与表单验证有关
        null 数据库可储存为空值 与数据库存储有关
    '''
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

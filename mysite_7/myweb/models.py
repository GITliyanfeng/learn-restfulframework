from django.db import models
from pygments.lexers import get_all_lexers  # 导入获取编程语言
from pygments.styles import get_all_styles  # 导入获取配色分隔
from pygments.lexers import get_lexer_by_name  # 通过名字获取编程语言
from pygments.formatters.html import HtmlFormatter  # 导入将数据格式化为HTML
from pygments import highlight  # 导入代码高亮
from django.contrib.auth.models import User

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
    # 一对多关系 主表查附表的时候  沟通的   节点  related_name='CodeSegments'   默认是 CodeSegment_set
    owner = models.ForeignKey(User, related_name='CodeSegments', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        # 变量 = 数据 and 正确区间 or 错误区间       如果数据为空返回错误区间  如果 数据为真返回 正确区间
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer=lexer, formatter=formatter)
        # 继承父类的save方法
        super(CodeSegment, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)

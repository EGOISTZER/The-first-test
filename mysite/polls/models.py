import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
# models.Model是一个类


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
# 每个字段都是 Field 类的实例 -
# 比如，字符字段被表示为 CharField ，
# 日期时间字段被表示为 DateTimeField 。

    def __str__(self):
        return self.question_text  # 当要打印自身时返回question_text

    # 编辑display
    @admin.display(
        boolean=True,       # true，false以图标形式展示
        ordering='pub_date',    # 按pub_date排序
        description='Published recently?'  # 改变描述
    )
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # 建立一对多关系,第一个参数是关联的主表,从而与主键建立联系.
    # 如果没建立主键则自动在表格里添加一个名叫id的字段
    # 第二个参数则是主表的字段被删除时，和他有关的子表字段也会被删除

    # 我们使用ForeignKey定义了一个关系。这将告诉Django，每个Choice对象都关联到一个Question对象
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

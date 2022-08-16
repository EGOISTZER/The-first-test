from django.contrib import admin

from .models import Question, Choice


# 使用StackInline设置Choice为内置，以块的形式内置
# 使用TabularInline设置Choice为内置，以表格的形式内置
# 'classes': ['collapse']设置该字段为折叠
class ChoiceInline(admin.TabularInline):
    model = Choice  # 选择要内嵌的类
    extra = 1       # 选择要额外留白多少个


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')  # 表单显示的属性
    list_filter = ['pub_date']  # 以pub_date作为过滤选项
    search_fields = ['question_text']  # 顶部添加搜索框，用来搜索question_text属性

    fieldsets = [
        (None,      {'fields': ['question_text']}),
        ("Date information", {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)

#
# # 创建fieldsets元组为属性设置标题
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,                {'fields': ['question_text']}),
#         ('Date information',  {'fields': ['pub_date']}),
#     ]
#
#
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)

#
# # 定义了Question模型属性排序是pub_date先然后才是question_text
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']
#
#
# admin.site.register(Question, QuestionAdmin)

# admin.site.register(Question)

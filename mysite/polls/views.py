from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
                pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
# ListView视图是用来显示一个对象列表
#  template_name是用来替代默认生成模板并告诉它用这个
# context_object_name则是用来替代context默认值
# 双下划线作为条件前置后面接条件,比如a__
# gt大于，lt小于，gte大于等于，lte小于等于


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

    # render()快捷用法
    # latest_question_list = Question.objects.order_by('pub_date')[:5]
    # context={'latest_question_list:latest_question_list'}
    # return render(request,'polls/index.html',context)
    #  请求，载入模板路径,内容

    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # #按照pub_date前五个进行排序
    # output = ', '.join([q.question_text for q in latest_question_list])
    # #在latest_question_list中循环q的值question_text,列表解析式
    # return HttpResponse(output)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
# DetailView用来显示一个特定类型对象的详细信息界面

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNoExist:
    #     raise Http404("Question does no exist")
    # return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))





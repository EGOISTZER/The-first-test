import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase


from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    # create 相当与filter+save
    return Question.objects.create(question_text=question_text, pub_date=time)


# Index测试
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        # 判断是否能正常访问polls：index
        self.assertEqual(response.status_code, 200)
        # 检查response中是否含有字段“No xxx able”
        self.assertContains(response, "No polls are available.")
        # 检查['laest_question_list']是否存在
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        # create_question 为快捷函数，在上方class外def中定义
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        # 数据库会在每个新的函数调用时重置，故上方函数中创建的问题已经消失
        create_question(question_text="Future question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_question(self):
        question1 = create_question(question_text="Past question1.", days=-30)
        question2 = create_question(question_text="Past question2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


# Question模型测试
class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_oid_question(self):
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        oid_question = Question(pub_date=time)
        self.assertIs(oid_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)



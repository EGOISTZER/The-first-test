from django.urls import path
from . import views

# 添加命名空间，防止多项目路径重名
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
# 第一个参数是路径，其中<>中为应该填入的值为int并命名为question_id
# 第二个参数在哪定义什么函数,比如第一条是指定view中的IndexView函数，
# 第三个参数是将这条路径命名为index，其他文件找路径时polls:index

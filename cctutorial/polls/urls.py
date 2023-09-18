from django.urls import path, re_path
from . import views


# polls/choices/
app_name = 'polls'
polls_url_base = 'polls/'

urlpatterns = [
    # ex: /
    path('', views.home, name='home'),
    # ex: /polls
    path(polls_url_base, views.index, name='index'),
    # ex: /polls/most-popular-choice/
    path(polls_url_base + 'most-popular-choice/', views.most_popular_choice, name='most-popular-choice'),
    # ex: /polls/choices/0010/
    re_path(polls_url_base + 'choices/(?P<pk>[0-9]{4})/', views.choices, name='choices'),  # 'choices/(?P<pk>[0-9]{1,4})/'
    # ex: /polls/choices/
    path(polls_url_base + 'choices/', views.choices, name='choices'),
    # ex: /polls/question/2023-09-16/ or /polls/question/2023/09/16/
    re_path(polls_url_base + 'question/(?P<pub_date>[0-9]{4}[-/][0-9]{2}[-/][0-9]{2})/', views.question, name='question'),
    # ex: /polls/question/
    path(polls_url_base + 'question/', views.question, name='question'),

    # from the tutorial
    # ex: /polls/5
    path(polls_url_base + '<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path(polls_url_base + '<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path(polls_url_base + '<int:question_id>/vote/', views.vote, name='vote'),
]

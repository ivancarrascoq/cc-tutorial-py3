from django.urls import path, re_path

from . import views

# polls/choices/
app_name = 'polls'
polls_url_base = 'polls/'

urlpatterns = [
    path('', views.home, name='home'),
    path(polls_url_base, views.index, name='index'),
    path(polls_url_base + 'most-popular/', views.most_popular_choice, name='most-popular-choice'),
    re_path(polls_url_base + 'choices/(?P<pk>[0-9]{4})/', views.choices, name='choices'), # http://localhost:8000/polls/choices/0011/
    path(polls_url_base + 'choices/', views.choices, name='choices'),
    re_path(polls_url_base + 'question/(?P<pub_date>[0-9]{4}[-/][0-9]{2}[-/][0-9]{2})/', views.question, name='question'),
]

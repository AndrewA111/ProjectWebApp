from django.urls import path
from question import views

app_name = 'question'

urlpatterns = [
    path('', views.question, name='question'),
    # path('question_list', views.question_list, name='question_list')
]
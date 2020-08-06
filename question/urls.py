from django.urls import path
from question import views

app_name = 'question'

urlpatterns = [
    path('submit/<slug:question_slug>/', views.question, name='question'),
    # path('question_list', views.question_list, name='question_list')
    path("upload/", views.upload, name='upload'),
    path("ajax_test/", views.ajax_test, name="ajax_test")

]

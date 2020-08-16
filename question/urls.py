from django.urls import path
from question import views


app_name = 'question'

urlpatterns = [
    # path('submit/<slug:question_slug>/', views.question, name='question'),
    # path('question_list', views.question_list, name='question_list')
    path("upload/", views.upload, name='upload'),
    path("ajax_upload/", views.ajax_upload, name="ajax_upload"),
    path("ajax_solve/", views.ajax_solve, name="ajax_solve"),
    path('create_profile/', views.create_profile, name="create_profile"),
    path('profile/<username>/', views.view_profile, name="view_profile"),
    path('courses/', views.course_list, name="course_list"),
    path('courses/<slug:course_slug>/', views.lesson_list, name="lesson_list"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', views.question_list, name="question_list"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/',
         views.question, name='question'),
]

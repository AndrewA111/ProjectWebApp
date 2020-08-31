from django.urls import path
from question import views


app_name = 'question'

urlpatterns = [
    # path('submit/<slug:question_slug>/', views.question, name='question'),
    # path('question_list', views.question_list, name='question_list')
    path("upload/", views.upload, name='upload'),
    path("courses/<slug:course_slug>/<slug:lesson_slug>/create_question/ajax_upload/",
         views.ajax_upload,
         name="ajax_upload"),
    path("courses/<slug:course_slug>/<slug:lesson_slug>/create_question/ajax_solve/",
         views.ajax_solve,
         name="ajax_solve"),
    # path("ajax_upload/", views.ajax_upload, name="ajax_upload"),
    # path("ajax_solve/", views.ajax_solve, name="ajax_solve"),
    path('create_profile/', views.create_profile, name="create_profile"),
    path('profile/<username>/', views.view_profile, name="view_profile"),
    path('courses/', views.course_list, name="course_list"),
    path('courses/create_course/', views.create_course, name='create_course'),
    path('courses/<slug:course_slug>/', views.course, name="lesson_list"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/move/<str:direction>/',
         views.move_lesson_ajax, name="move_lesson"),
    path('courses/<slug:course_slug>/create_lesson/', views.create_lesson, name='create_lesson'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', views.lesson, name="question_list"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/move/<str:direction>/',
         views.move_question_ajax, name="move_question"),

    path('courses/<slug:course_slug>/<slug:lesson_slug>/create_question/', views.upload, name="create_question"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/',
         views.question, name='question'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/bookmark/',
         views.bookmark_ajax, name='bookmark'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/ajax/',
         views.question_ajax, name='question_ajax'),
    path('markdown_convert/', views.markdown_ajax, name="markdown_convert"),
    path('bookmarks/', views.bookmarks, name="bookmarks"),
]

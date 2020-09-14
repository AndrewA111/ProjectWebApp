from django.urls import path
from question import views


app_name = 'question'

urlpatterns = [
    # Content hierarchy/navigation
    path('courses/', views.CourseListView.as_view(), name="course_list"),
    path('courses/<slug:course_slug>/', views.CourseView.as_view(), name="course"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', views.LessonView.as_view(), name="lesson"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/',
         views.QuestionView.as_view(), name='question'),

    # --- to be converted ---
    # path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/ajax/',
    #      views.question_ajax, name='question_ajax'),
    # path('courses/create_course/', views.create_course, name='create_course'),
    # path('courses/<slug:course_slug>/create_lesson/', views.create_lesson, name='create_lesson'),

    # Content ordering
    path('courses/<slug:course_slug>/<slug:lesson_slug>/move/<str:direction>/',
         views.move_lesson_ajax, name="move_lesson"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/move/<str:direction>/',
         views.move_question_ajax, name="move_question"),

    # Question Upload
    path('upload/<slug:course_slug>/<slug:lesson_slug>/',
         views.UploadView.as_view(), name="upload"),
    path("courses/<slug:course_slug>/<slug:lesson_slug>/create_question/ajax_solve/",
         views.ajax_solve, name="ajax_solve"),

    # Profile
    path('profile/<username>/', views.ProfileView.as_view(), name="view_profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('create_profile/', views.create_profile, name="create_profile"),

    # Bookmarking
    path('bookmarks/', views.BookmarksView.as_view(), name="bookmarks"),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/<slug:question_slug>/bookmark/',
         views.bookmark_ajax, name='bookmark'),

    # Markdown conversion via ajax
    path('markdown_convert/', views.markdown_ajax, name="markdown_convert"),
]
